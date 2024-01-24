#!/usr/bin/env python
#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE
#
#
import json
import yaml
import os
import shutil
import uuid
import pprint
import time
import subprocess
import concurrent.futures

from jinja2 import Template
from tabulate import tabulate
from tqdm import tqdm

from unskript_utils import *
from unskript_ctl_factory import ChecksFactory, ScriptsFactory
from unskript.legos.utils import CheckOutputStatus


# Implements Checks Class that is wrapper for All Checks Function
class Checks(ChecksFactory):
    TBL_CELL_CONTENT_PASS="\033[1m PASS \033[0m"
    TBL_CELL_CONTENT_SKIPPED="\033[1m SKIPPED \033[0m"
    TBL_CELL_CONTENT_FAIL="\033[1m FAIL \033[0m"
    TBL_CELL_CONTENT_ERROR="\033[1m ERROR \033[0m"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger.debug("Initialized Checks Class")
        if self._config.get_checks_params():
            self.checks_globals = self._config.get_checks_params().get('global')
            self.matrix = self.checks_globals.get('matrix')
        else:
            self.checks_globals = None
            self.matrix = None
        self.temp_jit_file = "/tmp/jit_script.py"
        self.check_names = []
        self.check_uuids = []
        self.connector_types = []
        self.status_list_of_dict = []
        self.uglobals = UnskriptGlobals()
        self._common = CommonAction()
        self.update_credentials_to_uglobal()
        self.uglobals['global'] = self.checks_globals

        for k,v in self.checks_globals.items():
            os.environ[k] = json.dumps(v)

    def run(self, **kwargs):
        if "checks_list" not in kwargs:
            self.logger.error("ERROR: checks_list is a mandatory parameter to be sent, cannot run without the checks list")
            raise ValueError("Parameter check_list is not present in the argument, please call run with the check_list=[list_of_checks]")
        checks_list = kwargs.get('checks_list')
        if len(checks_list) == 0:
            self.logger.error("ERROR: Checks list is empty, Cannot run anything")
            raise ValueError("Checks List is empty!")

        checks_list = self.create_checks_for_matrix_argument(checks_list)
        checks_list = self.insert_task_lines(checks_list=checks_list)
        if not self._create_jit_script(checks_list=checks_list):
            self.logger.error("ERROR: Cannot create JIT script to run the checks, please look at logs")
            raise ValueError("Unable to create JIT script to run the checks")
        outputs = None
        try:
            if "/tmp" not in sys.path:
                sys.path.append("/tmp/")
            from jit_script import do_run_
            temp_output = do_run_()
            output_list = []
            for o in temp_output.split('\n'):
                if not o:
                    continue
                d = json.loads(json.dumps(o))
                if isinstance(d, dict) is False:
                    d = json.loads(d)
                d['name'] = self.check_names[self.check_uuids.index(d.get('id'))]
                output_list.append(d)
            outputs = output_list
        except Exception as e:
            self.logger.error(e)
            self._error(str(e))
        finally:
            self._common.update_exec_id()
            output_file = os.path.join(UNSKRIPT_EXECUTION_DIR, self.uglobals.get('exec_id')) + '_output.txt'
            if not outputs:
                self.logger.error("Output is None from check's output")
                self._error('OUTPUT IS EMPTY FROM CHECKS RUN!')
                sys.exit(0)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json.dumps(outputs))
            if len(outputs) == 0:
                self.logger.error(f"Output from checks execution is empty, pls check {self.temp_jit_file}")
                self._error(f" Output from checks execution is empty, pls check {self.temp_jit_file}")
                return

        self.display_check_result(checks_output=outputs)
        self.uglobals['status_of_run'] = self.status_list_of_dict

        return self.status_list_of_dict

    def parse_failed_objects(self, failed_object):
        retVal = "N/A"
        for line in failed_object:
            if "forbidden" in line:
                retVal = "Forbidden "
            if "permission" in line:
                retVal = "Access Denied"
            if "not reachable" in line:
                retVal = "Network error"
        return retVal


    def display_check_result(self, checks_output):
        if not checks_output:
            self.logger.error("Check's Output is None!")
            self._error(" Check's Output is None")
            return

        result_table = [["Checks Name", "Result", "Failed Count", "Error"]]
        status_dict = {}
        status_dict['runbook'] = os.path.join(UNSKRIPT_EXECUTION_DIR, self.uglobals.get('exec_id') + '_output.txt')
        status_dict['result'] = []
        if self.uglobals.get('skipped'):
            for check_name,connector in self.uglobals.get('skipped'):
                result_table.append([
                    check_name,
                    self.TBL_CELL_CONTENT_SKIPPED,
                    "N/A",
                    "Credential Incomplete"
                ])
                status_dict['result'].append([
                    check_name,
                    "",
                    connector,
                    'ERROR'
                    ])
        idx = 0
        ids = self.check_uuids
        failed_result_available = False
        failed_result = {}
        checks_output = self.output_after_merging_checks(checks_output, self.check_uuids)
        for result in checks_output:
            if result.get('skip') and result.get('skip') is True:
                idx += 1
                continue
            payload = result
            try:
                if ids and CheckOutputStatus(payload.get('status')) == CheckOutputStatus.SUCCESS:
                    result_table.append([
                        self.check_names[idx],
                        self.TBL_CELL_CONTENT_PASS,
                        0,
                        'N/A'
                        ])
                    status_dict['result'].append([
                        self.check_names[idx],
                        ids[idx],
                        self.connector_types[idx],
                        'PASS']
                        )
                elif ids and CheckOutputStatus(payload.get('status')) == CheckOutputStatus.FAILED:
                    failed_objects = payload.get('objects')
                    c_name = self.connector_types[idx] + ':' + self.check_names[idx]
                    failed_result[c_name] = failed_objects
                    result_table.append([
                        self.check_names[idx],
                        self.TBL_CELL_CONTENT_FAIL,
                        len(failed_objects),
                        self.parse_failed_objects(failed_object=failed_objects)
                        ])
                    failed_result_available = True
                    status_dict['result'].append([
                        self.check_names[idx],
                        ids[idx],
                        self.connector_types[idx],
                        'FAIL'
                        ])
                elif ids and CheckOutputStatus(payload.get('status')) == CheckOutputStatus.RUN_EXCEPTION:
                    if payload.get('error') is not None:
                        failed_objects = payload.get('error')
                        if isinstance(failed_objects, str) is True:
                            failed_objects = [failed_objects]
                        c_name = self.connector_types[idx] + ':' + self.check_names[idx]
                        failed_result[c_name] = failed_objects
                    error_msg = payload.get('error') if payload.get('error') else self.parse_failed_objects(failed_object=failed_objects)
                    result_table.append([
                        self.check_names[idx],
                        self.TBL_CELL_CONTENT_ERROR,
                        0,
                        pprint.pformat(error_msg, width=30)
                        ])
                    status_dict['result'].append([
                        self.check_names[idx],
                        ids[idx],
                        self.connector_types[idx],
                        'ERROR'
                        ])
            except Exception as e:
                self.logger.error(e)
                pass
            idx += 1

        print("")
        print(tabulate(result_table, headers='firstrow', tablefmt='fancy_grid'))

        if failed_result_available is True:
            self.uglobals['failed_result'] = {'result': []}
            for k,v in failed_result.items():
                d = {}
                if not v:
                    continue
                d[k] = {'failed_object': v}
                self.uglobals['failed_result']['result'].append(d)

        print("")
        self.status_list_of_dict.append(status_dict)
        for k,v in failed_result.items():
            check_name = '\x1B[1;4m' + k + '\x1B[0m'
            print(check_name)
            self._error("Failed Objects:")
            print(yaml.safe_dump(v))
            print('\x1B[1;4m', '\x1B[0m')
        return



    def output_after_merging_checks(self, outputs: list, ids: list) -> list:
        """output_after_merging_checks: this function combines the output from duplicated
        checks and stores the combined output.
        TBD: What if one duplicated check returns an ERROR
        """
        new_outputs = []
        # Remove empty strings
        filtered_output = []
        for output in outputs:
            if not output:
                continue
            filtered_output.append(output)

        outputs = filtered_output
        if self.uglobals.get('uuid_mapping') is None:
            return outputs

        index = 0
        while index < len(outputs):
            if self.uglobals['uuid_mapping'].get(ids[index]) is None:
                new_outputs.append(outputs[index])
                index = index+1
            else:
                parent_index = index - 1
                while index < len(outputs):
                    if self.uglobals['uuid_mapping'].get(ids[index]):
                        outputs[index]['skip'] = True
                        new_outputs.append(outputs[index])
                        index = index + 1
                    else:
                        break
                combined_output = self.calculate_combined_check_status(outputs[parent_index:index])
                # Combined output should be the output of the parent check, so
                # overwrite it.
                #print(f'parent_index {parent_index}, index {index}, combined_output {combined_output}')
                new_outputs[parent_index] = combined_output
        return new_outputs

    def calculate_combined_check_status(self, outputs:list):
        combined_output = {}
        status = CheckOutputStatus.SUCCESS
        failed_objects = []
        error = None
        for output in outputs:
            if CheckOutputStatus(output.get('status')) == CheckOutputStatus.FAILED:
                status = CheckOutputStatus.FAILED
                failed_objects.append(output.get('objects'))
            elif CheckOutputStatus(output.get('status')) == CheckOutputStatus.RUN_EXCEPTION:
                status = CheckOutputStatus.RUN_EXCEPTION
                error = output.get('error')

        combined_output['status'] = status
        combined_output['objects'] = failed_objects
        combined_output['error'] = error
        return combined_output

    def _create_jit_script(self, checks_list: list = None):
        if not checks_list:
            self.logger.error("Checks List Cannot be empty. Please verify the checks_list is valid")
            return False

        with open(self.temp_jit_file, 'w', encoding='utf-8') as f:
            f.write(self.get_first_cell_content(checks_list))
            f.write('\n\n')
            for idx,c in enumerate(checks_list[:]):
                idx += 1
                check_name = f"def check_{idx}():"
                f.write(check_name + '\n')
                f.write('    global w' + '\n')
                for line in c.get('code'):
                    line = line.replace('\n', '')
                    for l in line.split('\n'):
                        l = l.replace('\n', '')
                        if l.startswith("from __future__"):
                            continue
                        f.write('    ' + l.replace('\n', '') + '\n')
            f.write('\n')
            # Lets create the last cell content
            f.write('def last_cell():' + '\n')
            last_cell_content = self.get_last_cell_content()
            for line in last_cell_content.split('\n'):
                f.write('    ' + line + '\n')
            f.write('\n')

            post_check_content = self.get_after_check_content(len(checks_list))
            f.write(post_check_content + '\n')

        if os.path.exists(self.temp_jit_file) is True:
            return True

        return False


    def get_first_cell_content(self, list_of_checks: list):
        if len(list_of_checks) == 0:
            return None
        self.check_uuids, self.check_names, self.connector_types = self._common.get_code_cell_name_and_uuid(list_of_actions=list_of_checks)
        first_cell_content = self._common.get_first_cell_content()

        if self.checks_globals and len(self.checks_globals):
            for k,v in self.checks_globals.items():
                if k == 'matrix':
                    continue
                if isinstance(v,str) is True:
                    first_cell_content += f'{k} = \"{v}\"' + '\n'
                else:
                    first_cell_content += f'{k} = {v}' + '\n'
        if self.matrix:
            for k,v in self.matrix.items():
                if v:
                    for index, value in enumerate(v):
                        first_cell_content += f'{k}{index} = \"{value}\"' + '\n'
        first_cell_content += f'''w = Workflow(env, secret_store_cfg, None, global_vars=globals(), check_uuids={self.check_uuids})'''

        return first_cell_content

    def get_last_cell_content(self):
        with open(os.path.join(os.path.dirname(__file__), 'templates/last_cell_content.j2'), 'r') as f:
            content_template = f.read()

        template = Template(content_template)
        return  template.render()


    def get_after_check_content(self, len_of_checks):
        with open(os.path.join(os.path.dirname(__file__), 'templates/template_script.j2'), 'r') as f:
            content_template = f.read()

        template = Template(content_template)
        return  template.render(num_checks=len_of_checks)

    def insert_task_lines(self, checks_list: list):
        if checks_list and len(checks_list):
            return self._common.insert_task_lines(list_of_actions=checks_list)

    def create_checks_for_matrix_argument(self, checks: list):
        checks_list = []
        if self.checks_globals and len(self.checks_globals):
            checks_list = self._common.create_checks_for_matrix_argument(actions=checks, matrix=self.matrix)

        return checks_list


# This class implements Script interface for ScriptsFactory.
class Script(ScriptsFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger.debug("Initialized Script Class")
        self.uglobals = UnskriptGlobals()

    def run(self, **kwargs):
        if 'script' not in kwargs:
            self.logger.error("ERROR: script is a mandatory parameter to be sent, cannot run without the scripts list")
            raise ValueError("Parameter script is not present in the argument, please call run with the scripts_list=[scripts]")
        script = kwargs.get('script')
        if not self.uglobals.get('CURRENT_EXECUTION_RUN_DIRECTORY'):
            output_dir = create_execution_run_directory()
        else:
            output_dir = self.uglobals.get('CURRENT_EXECUTION_RUN_DIRECTORY')
        output_file = UNSKRIPT_SCRIPT_RUN_OUTPUT_FILE_NAME
        output_file_txt = os.path.join(output_dir, output_file + ".txt")
        output_file_json = os.path.join(output_dir, output_file + ".json")
        current_env = os.environ.copy()
        current_env[UNSKRIPT_SCRIPT_RUN_OUTPUT_DIR_ENV] = output_dir
        if isinstance(script, list) is False:
            script = [script]
        script_to_print = ' '.join(script)
        self._banner(f"Execution script {script_to_print}")
        self._banner(f"OUTPUT FILE {output_file_txt}")
        st = time.time()
        status = "SUCCESS"
        error = None
        try:
            with open(output_file_txt, "w") as f:
                subprocess.run(script,
                               check=True,
                               env=current_env,
                               shell=True,
                               stdout=f,
                               stderr=f)
        except Exception as e:
            self._error(f'{" ".join(script)} failed, {e}')
            error = str(e)
            status = "FAIL"

        et = time.time()
        elapsed_time = et - st

        json_output = {}
        json_output['status'] = status
        json_output['time_taken'] = f'{elapsed_time:.2f}'
        json_output['error'] = error
        json_output['output_file'] = output_file_txt
        json_output['compress'] = True

        try:
            with open(output_file_json, 'w') as f:
                json.dump(json_output, fp=f)
        except Exception as e:
            self._error(str(e))
            sys.exit(0)


class CommonAction(ChecksFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_code_cell_name_and_uuid(self, list_of_actions: list):
        action_uuids, action_names, connector_types = [], [], []
        if len(list_of_actions) == 0:
            self.logger.error("List of actions is empty!")
            return action_uuids, action_names

        for action in list_of_actions:
            metadata = action.get('metadata')
            action_uuid = action.get('uuid')
            if metadata:
                action_name = metadata.get('name') if metadata.get('name') else metadata.get('action_entry_function')
                connector_type = metadata.get('action_type').replace('LEGO_TYPE_', '').lower()

                if action_uuid:
                    action_uuids.append(action_uuid)
                if action_name:
                    action_names.append(action_name)
                if connector_type:
                    connector_types.append(connector_type)

        self.logger.debug(f"Returning {len(action_uuids)} UUIDs and {len(action_names)} names")
        return action_uuids, action_names, connector_types

    def update_exec_id(self):
        self.uglobals = UnskriptGlobals()
        if not self.uglobals.get('exec_id'):
            self.uglobals['exec_id'] = str(uuid.uuid4())


    def get_first_cell_content(self):
        runbook_params = {}
        if os.environ.get('ACA_RUNBOOK_PARAMS') is not None:
            runbook_params = json.loads(os.environ.get('ACA_RUNBOOK_PARAMS'))
        runbook_variables = ''
        if runbook_params:
            for k, v in runbook_params.items():
                runbook_variables = runbook_variables + \
                    f"{k} = nbParamsObj.get('{k}')" + '\n'

        with open(os.path.join(os.path.dirname(__file__), 'templates/first_cell_content.j2'), 'r') as f:
            first_cell_content_template = f.read()

        template = Template(first_cell_content_template)
        first_cell_content = template.render(runbook_params=runbook_params,
                                             runbook_variables=runbook_variables)
        return first_cell_content

    def create_checks_for_matrix_argument(self, actions: list, matrix: dict):
        """create_checks_for_matrix_argument: This function generates the inputJson line of
        code for a check. It handles the matrix case wherein you need to use the
        appropriate variable name for argument assignment.
        """
        self.matrix = matrix
        action_list = []
        for action in actions:
            input_schema = action.get('inputschema')
            if input_schema is None:
                action_list.append(action)
                continue
            add_check_to_list = True

            input_json_line = ''
            try:
                schema = input_schema[0]
                if schema.get('properties'):
                    for key in schema.get('properties').keys():
                        # Check if the property is a matrix argument.
                        # If thats the case, replicate the check the number
                        # of entries in  that argument.
                        duplicate_count = 1
                        if self.matrix:
                            matrix_value = self.matrix.get(key)
                            if matrix_value is not None:
                                duplicate_count += len(matrix_value)
                                # Duplicate this check len(matrix_argument) times.
                                # Also, for each check, you need to use a different
                                # argument, so store that in a field named
                                # matrixinputline
                                # UUID Mapping need to initialized before assinging it a value!
                                if not isinstance(self.uglobals.get('uuid_mapping'), dict):
                                    self.uglobals['uuid_mapping'] = {}
                                is_first = True
                                for dup in range(duplicate_count-1):
                                    add_check_to_list = False
                                    input_json_line = ''
                                    input_json_line += f"\"{key}\":  \"{matrix_value[dup]}\" ,"
                                    newcheck = action.copy()
                                    if is_first is False:
                                        # Maintain the uuid mapping that this uuid is the same as
                                        # as the one its copied from.
                                        new_uuid = str(uuid.uuid4())
                                        self.uglobals["uuid_mapping"][new_uuid] = action["uuid"]
                                        newcheck['uuid'] = new_uuid
                                        newcheck['id'] = str(uuid.uuid4())[:8]
                                        #print(f'Adding duplicate check {new_uuid}, parent_uuid {check.get("uuid")}')
                                    newcheck['matrixinputline'] = input_json_line.rstrip(',')
                                    action_list.append(newcheck)
                                    is_first = False
            except Exception as e:
                self.logger.error(f"EXCEPTION {e}")
                self._error(str(e))
                pass
            if add_check_to_list:
                    action_list.append(action)

        return action_list

    def insert_task_lines(self, list_of_actions: list):
        self.update_credentials_to_uglobal()

        for action in list_of_actions:
            s_connector = action.get('metadata').get('action_type')
            s_connector = s_connector.replace('LEGO', 'CONNECTOR')
            cred_name, cred_id = None, None
            for k,v in self.uglobals.get('default_credentials').items():
                if k == s_connector:
                    cred_name, cred_id = v.get('name'), v.get('id')
                    break
            if cred_name is None or cred_id is None:
                if self.uglobals.get('skipped') is None:
                    self.uglobals['skipped'] = []
                _t = [action.get('name'), s_connector]
                if _t not in self.uglobals.get('skipped'):
                    self.uglobals['skipped'].append(_t)
                    continue
            task_lines = '''
task.configure(printOutput=True)
task.configure(credentialsJson=\'\'\'{
        \"credential_name\":''' + f" \"{cred_name}\"" + ''',
        \"credential_type\":''' + f" \"{s_connector}\"" + '''}\'\'\')
'''
            input_json = self.replace_input_with_globals(action)
            if input_json:
                task_lines += input_json

            try:
                c = action.get('code')
                idx = c.index("task = Task(Workflow())")
                if c[idx+1].startswith("task.configure(credentialsJson"):
                    # With credential caching now packged in, we need to
                    # Skip the credential line and let the normal credential
                    # logic work.
                    c = c[:idx+1] + task_lines.split('\n') + c[idx+2:]
                else:
                    c = c[:idx+1] + task_lines.split('\n') + c[idx+1:]
                action['code'] = []
                for line in c[:]:
                    action['code'].append(str(line + "\n"))

                action['metadata']['action_uuid'] = action['uuid']
                action['metadata']['name'] = action['name']

            except Exception as e:
                self.logger.error(f"Unable to insert Task lines {e}")
                self._error(e)
                sys.exit(0)

        return list_of_actions


    def replace_input_with_globals(self, action: dict):
        inputSchema = action.get('inputschema')
        retval = None
        if not inputSchema:
            return retval
        input_json_start_line = '''
task.configure(inputParamsJson=\'\'\'{
        '''
        input_json_end_line = '''}\'\'\')
        '''
        input_json_line = ''
        try:
            schema = inputSchema[0]
            if schema.get('properties'):
                for key in schema.get('properties').keys():
                    if key in self.uglobals.get('global').keys():
                        value = self.uglobals.get('global').get(key)
                        if value:
                            input_json_line += f"\"{key}\":  \"{value}\" ,"
                        else:
                            input_json_line += f"\"{key}\":  \"{key}\" ,"
        except Exception as e:
            self.logger.error(e)
            self._error(str(e))
        # Handle Matrix argument
        matrix_argument_line = action.get('matrixinputline')
        if matrix_argument_line:
            input_json_line += matrix_argument_line
        retval = input_json_start_line + input_json_line.rstrip(',') + '\n' + input_json_end_line

        return retval



# Implements Info class that is a wrapper to run all info gathering function
class InfoAction(ChecksFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger.debug("Initialized InfoAction class")
        if self._config.get_info_action_params():
            self.info_globals = self._config.get_info_action_params().get('global')
            self.matrix = self.info_globals.get('matrix')
        else:
            self.info_globals = None
            self.matrix = None
        self.temp_jit_dir = '/tmp/jit'
        self.temp_jit_base_name = 'jit_info_script'
        self._common = CommonAction()
        self.uglobals = UnskriptGlobals()
        self.uglobals['global'] = self.info_globals

        for k,v in self.info_globals.items():
            os.environ[k] =  json.dumps(v)

    def run(self, **kwargs):
        if "action_list" not in kwargs:
            self.logger.error("ERROR: action_list is a mandatory parameter to be sent, cannot run without the action_list")
            raise ValueError("Parameter action_list is not present in the argument, please call run with the action_list=[list_of_action]")
        action_list = kwargs.get('action_list')
        if len(action_list) == 0:
            self.logger.error("ERROR: Action list is empty, Cannot run anything")
            raise ValueError("Action List is empty!")

        self.action_uuid, self.check_names, self.connector_types = \
                self._common.get_code_cell_name_and_uuid(list_of_actions=action_list)

        action_list = self.create_checks_for_matrix_argument(action_list)
        action_list = self.insert_task_lines(list_of_actions=action_list)

        self.uglobals['info_action_results'] = {}
        if not self._create_jit_script(action_list=action_list):
            self.logger.error("Cannot create JIT scripts to run the checks, please look at logs")
            raise ValueError("Unable to create JIT script to run the checks")

        # Internal routine to run through all python JIT script and return the output
        def _execute_script(script, idx):
            check_name = self.check_names[idx]
            connector_name = self.connector_types[idx]
            result_key = f"{connector_name}/{check_name}"
            if not self.uglobals['info_action_results'].get(result_key):
                self.uglobals['info_action_results'][result_key] = []
            try:
                result = subprocess.run(['python', script], capture_output=True, check=True, text=True)
                self.logger.debug(result.stdout)
                if len(self.uglobals["info_action_results"].get(result_key)) != 0:
                    self.uglobals['info_action_results'][result_key].append(result.stdout)
                else:
                    self.uglobals['info_action_results'][result_key] = result.stdout
            except subprocess.CalledProcessError as e:
                sys.logger.error(f"Error executing {script}: {str(e)}")
                raise ValueError(e)
            finally:
                return result.stdout

        script_files = [f for f in os.listdir(self.temp_jit_dir) if f.endswith('.py')]
        with concurrent.futures.ThreadPoolExecutor() as executor, tqdm(total=len(script_files), desc="Running") as pbar:
            futures = {executor.submit(_execute_script, os.path.join(self.temp_jit_dir, script), idx): idx for idx, script in enumerate(script_files)}
            # Wait for all scripts to complete
            for _ in concurrent.futures.as_completed(futures):
                pbar.update(1)

        # Lets remove the directory if it exists
        try:
            shutil.rmtree(self.temp_jit_dir)
        except OSError as e:
            self.logging.error(str(e))

        self.display_action_result()


    def _create_jit_script(self, action_list: list = None):
        if not action_list:
            self.logger.error("Action cannot be Empty. Nothing to create!")
            return False

        try:
            shutil.rmtree(self.temp_jit_dir)
        except:
            pass
        os.makedirs(self.temp_jit_dir, exist_ok=True)
        first_cell_content = self.get_first_cell_content()
        for index, action in enumerate(action_list):
            jit_file = os.path.join(self.temp_jit_dir, self.temp_jit_base_name + str(index) + '.py')
            with open(jit_file, 'w') as f:
                f.write(first_cell_content)
                f.write('\n\n')
                f.write('def action():' + '\n')
                f.write('    global w' + '\n')
                for lines in action.get('code'):
                    lines = lines.rstrip().split('\n')
                    for line in lines:
                        line = line.replace('\n', '')
                        if line.startswith("from __future__"):
                            continue
                        f.write('    ' + line.rstrip() + '\n')
                f.write('\n')
                # Now the Main section
                f.write('if __name__ == "__main__":' + '\n')
                f.write('    action()')

        if os.path.exists(self.temp_jit_dir) is True:
            return True

        return False

    def display_action_result(self):
        if self.uglobals.get('info_action_results'):
            for k,v in self.uglobals.get('info_action_results').items():
                self._banner('')
                print(bcolors.UNDERLINE + bcolors.HIGHLIGHT + k + bcolors.ARG_END + bcolors.ENDC)
                print('\n')
                print(v)
                print('###')
        else:
            self.logger.info("Information gathering actions: No Results to display")


    def get_first_cell_content(self):
        first_cell_content = self._common.get_first_cell_content()

        if self.info_globals and len(self.info_globals):
            for k,v in self.info_globals.items():
                if k == 'matrix':
                    continue
                if isinstance(v, str) is True:
                    first_cell_content += f'{k} = \"{v}\"' + '\n'
                else:
                    first_cell_content += f'{k} = {v}' + '\n'

        if self.matrix:
            for k,v in self.matrix.items():
                if v:
                    for index, value in enumerate(v):
                        first_cell_content += f'{k}{index} = \"{value}\"' + '\n'

        first_cell_content += '''w = Workflow(env, secret_store_cfg, None, global_vars=globals(), check_uuids=None)'''
        return first_cell_content

    def insert_task_lines(self, list_of_actions: list):
        if list_of_actions and len(list_of_actions):
            return self._common.insert_task_lines(list_of_actions=list_of_actions)

    def create_checks_for_matrix_argument(self, list_of_actions: list):
        action_list = []
        if self.info_globals and len(self.info_globals):
            action_list = self._common.create_checks_for_matrix_argument(actions=list_of_actions,
                                                                         matrix=self.matrix)
        return action_list


