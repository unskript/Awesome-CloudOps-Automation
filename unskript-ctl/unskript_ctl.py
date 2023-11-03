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
import os
import sys
import glob
import json
import pprint
import time
import re
import uuid
import psutil
import pprint
import subprocess
import yaml
import nbformat
import ZODB
import ZODB.FileStorage

from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser, REMAINDER, SUPPRESS
from db_utils import *
from tabulate import tabulate
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
from unskript.legos.utils import CheckOutputStatus
from unskript_ctl_gen_report import *
from unskript_ctl_debug import *
from unskript_ctl_show import * 
from unskript_ctl_list import *
from ZODB import DB
from unskript_utils import *

# This python client can be used to
# 1. List all available runbooks
# 2. Run the Runbook and prints out result of the execution

# Note:
# This program assumes the following
# * The Runbooks are located in $HOME/runbooks folder
#   This assumption is valid for unSkript docker use-case.
# * This script assumes the system has all the python dependent libraries
#   installed before using this script.

# LIST OF CONSTANTS USED IN THIS FILE
# UNSKRIPT_GLOBALS = {}
GLOBAL_CONFIG_PATH="/etc/unskript/unskript_ctl_config.yaml"
ZODB_DB_PATH="/var/unskript/snippets.db"
TBL_HDR_CHKS_NAME="\033[36m Checks Name \033[0m"
TBL_HDR_CHKS_PASS="\033[32m Passed Checks \033[0m"
TBL_HDR_CHKS_FAIL="\033[35m Failed Checks \033[0m"
TBL_HDR_CHKS_ERROR="\033[31m Errored Checks \033[0m"
TBL_HDR_RBOOK_NAME="\033[36m Runbook Name \033[0m"
TBL_HDR_CHKS_COUNT="\033[32m Checks Count (Pass/Fail/Error) (Total checks run) / (Skipped checks) \033[0m"
TBL_CELL_CONTENT_PASS="\033[1m PASS \033[0m"
TBL_CELL_CONTENT_SKIPPED="\033[1m SKIPPED \033[0m"
TBL_CELL_CONTENT_FAIL="\033[1m FAIL \033[0m"
TBL_CELL_CONTENT_ERROR="\033[1m ERROR \033[0m"


# parser = ArgumentParser(prog='unskript-ctl')

def load_or_create_global_configuration():
    """load_global_configuration This function reads the unskript_global.yaml file from /data
       and sets os.env variables which we shall use it in the subsequent functions.
       :rpath: None
    """
    if os.path.exists(GLOBAL_CONFIG_PATH) is True:
        # READ EXISTING FILE AND SET ENV VARIABLES
        with open(GLOBAL_CONFIG_PATH, 'r') as f:
            config_yaml = yaml.safe_load(f)

        if config_yaml.get('checks'):
            if config_yaml.get('checks').get('arguments'):
                if config_yaml.get('checks').get('arguments').get('global'):
                    UNSKRIPT_GLOBALS['global'] = config_yaml.get('checks').get('arguments').get('global')
                    for k, v in config_yaml.get('checks').get('arguments').get('global').items():
                        os.environ[k] = json.dumps(v)

def insert_first_and_last_cell(nb: nbformat.NotebookNode) -> nbformat.NotebookNode:
    """insert_first_and_last_cell This function inserts the first cell (unskript internal)
           and the last cell to a given notebook and returns the NotebookNode object back.

       :type nb: NotebookNode
       :param nb: NotebookNode Object that has the runbook content in it

       :rtype: NotebookNode that has the first and the last cell inserted in it
    """
    if nb is None:
        return None

    ids = get_code_cell_action_uuids(nb.dict())
    # Firstcell content. Here the workflow will take the UUIDS that we got from
    # get_code_cell_action_uuids

    # FIXME: NEED TO CREATE FIRST CELL VARIABLES BASED ON ENV VARIABLE SET IN THE CONFIG FILE
    runbook_params = {}
    if os.environ.get('ACA_RUNBOOK_PARAMS') is not None:
        runbook_params = json.loads(os.environ.get('ACA_RUNBOOK_PARAMS'))
    runbook_variables = ''


    if runbook_params:
        for k, v in runbook_params.items():
            runbook_variables = runbook_variables + \
                f"{k} = nbParamsObj.get('{k}')" + '\n'
    first_cell_content = f'''\
import json
from unskript import nbparams
from unskript.fwk.workflow import Task, Workflow
from unskript.secrets import ENV_MODE, ENV_MODE_LOCAL

env = {{"ENV_MODE": "ENV_MODE_LOCAL"}}
secret_store_cfg = {{"SECRET_STORE_TYPE": "SECRET_STORE_TYPE_LOCAL"}}

paramDict = {runbook_params}
paramsJson = json.dumps(paramDict)
nbParamsObj = nbparams.NBParams(paramsJson)
{runbook_variables}
'''
    if UNSKRIPT_GLOBALS.get('global') and len(UNSKRIPT_GLOBALS.get('global')):
        for k,v in UNSKRIPT_GLOBALS.get('global').items():
            if isinstance(v,str) is True:
                first_cell_content += f'{k} = \"{v}\"' + '\n'
            else:
                first_cell_content += f'{k} = {v}' + '\n'

    first_cell_content += f'''
w = Workflow(env, secret_store_cfg, None, global_vars=globals(), check_uuids={ids})'''

    # Firstcell content. This is a static content
    last_cell_content = '''\
from unskript.legos.utils import CheckOutput, CheckOutputStatus


try:
    if 'w' in globals():
        if w.check_run:
            for id,output in w.check_output.items():
                output = json.loads(output)
                output['id'] = id
                print(json.dumps(output))
        else:
            print(json.dumps("Not a check run"))
    else:
        print(json.dumps("ERROR: Internal Error, Workflow is missing"))
except Exception as e:
    print(f"Internal error {{e}}")
'''

    cells = nb.dict().get('cells')
    if len(cells) == 0:
        # Empty runbook, nothing to be done. return back
        #print("ERROR: Runbook seems empty, nothing to run")
        return nb

    if cells[0].get('cell_type') == 'code':
        tags = None
        if cells[0].get('metadata').get('tags') is not None:
            if len(cells[0].get('metadata').get('tags')) != 0:
                tags = cells[0].get('metadata').get('tags')[0]

        # If we have the first cell present, remove it before inserting the new one
        if "unSkript:nbParam" == tags:
            nb['cells'].remove(nb['cells'][0])

    # First Cell insertion
    nb['cells'].insert(0, nbformat.v4.new_code_cell(
        first_cell_content, id='firstcell'))
    # Last Cell insertion
    nb['cells'].extend(
        [nbformat.v4.new_code_cell(last_cell_content, id='lastcell')])

    return nb



def run_ipynb(filename: str, status_list_of_dict: list = None, filter: str = None):
    """run_ipynb This function takes the Runbook name and executes it
           using nbclient.execute()

       :type filename: str
       :param filename: Runbook name

       :rtype: None, Runbook execution will be displayed
    """
    hardcoded_checks = [
    "Get Unscheduled K8s Pods due to Node",
    "Get Node-affinity related failures",
    "Get Failed Readiness Probes",
    "Get Failed Liveness Probes",
    "Get K8s DaemonSets Missing on Node"
    ]
    nb = read_ipynb(filename)

    # We store the Status of runbook execution in status_dict
    status_dict = {}
    status_dict['runbook'] = filename
    status_dict['result'] = []
    r_name = '\x1B[1;20;42m' + "Executing Runbook -> " + \
        filename.strip() + '\x1B[0m'
    print(r_name)


    if nb is None:
        raise Exception("Unable to Run the Ipynb file, internal service error")

    nb = insert_first_and_last_cell(nb)

    client = NotebookClient(nb=nb, kernel_name="python3")

    try:
        execution = client.execute()
    except CellExecutionError as e:
        raise e
    finally:
        os.remove(filename)
        output_file = filename
        output_file = output_file.replace('.ipynb', '_output.ipynb')
        nbformat.write(nb, output_file)
        new_nb = None
        with open(output_file, "r") as f:
            new_nb = nbformat.read(f, as_version=4)
        outputs = get_last_code_cell_output(new_nb.dict())
        if len(outputs) == 0:
            print("ERROR: Output of the cell execution is empty. Is the credential configured?")

    ids = get_code_cell_action_uuids(nb.dict())
    result_table = [["Checks Name", "Result", "Failed Count", "Error"]]
    if UNSKRIPT_GLOBALS.get('skipped'):
        for check_name,connector in UNSKRIPT_GLOBALS.get('skipped'):
            result_table.append([
                check_name,
                TBL_CELL_CONTENT_SKIPPED,
                "N/A",
                "Credential Incomplete"
            ])
            status_dict['result'].append([
                check_name,
                "",
                connector,
                'ERROR'
                ])

    results = []
    if ids:
        results = outputs
    idx = 0
    failed_result_available = False
    failed_result = {}

    if ids:
        for output in outputs:
            r = output.get('text')
            for result in r.split('\n'):
                if result == '':
                    continue
                payload = json.loads(result)

                try:
                    if ids and CheckOutputStatus(payload.get('status')) == CheckOutputStatus.SUCCESS:
                        result_table.append([
                            get_action_name_from_id(ids[idx], nb.dict()),
                            TBL_CELL_CONTENT_PASS,
                            0,
                            'N/A'
                            ])
                        status_dict['result'].append([
                            get_action_name_from_id(ids[idx], nb.dict()),
                            ids[idx],
                            get_connector_name_from_id(ids[idx], nb.dict()),
                            'PASS']
                            )
                    elif ids and CheckOutputStatus(payload.get('status')) == CheckOutputStatus.FAILED:
                        failed_objects = payload.get('objects')
                        c_name = get_connector_name_from_id(ids[idx], nb.dict()) + ':' + get_action_name_from_id(ids[idx], nb.dict())
                        failed_result[c_name] = failed_objects
                        result_table.append([
                            get_action_name_from_id(ids[idx], nb.dict()),
                            TBL_CELL_CONTENT_FAIL,
                            len(failed_objects),
                            'N/A'
                            ])
                        failed_result_available = True
                        status_dict['result'].append([
                            get_action_name_from_id(ids[idx], nb.dict()),
                            ids[idx],
                            get_connector_name_from_id(ids[idx], nb.dict()),
                            'FAIL'
                            ])
                    elif ids and CheckOutputStatus(payload.get('status')) == CheckOutputStatus.RUN_EXCEPTION:
                        if payload.get('error') is not None:
                            failed_objects = payload.get('error')
                            c_name = get_connector_name_from_id(ids[idx], nb.dict()) + ':' + get_action_name_from_id(ids[idx], nb.dict())
                            failed_result[c_name] = failed_objects
                        result_table.append([
                            get_action_name_from_id(ids[idx], nb.dict()),
                            TBL_CELL_CONTENT_ERROR,
                            0,
                            pprint.pformat(payload.get('error'), width=30)
                            ])
                        status_dict['result'].append([
                            get_action_name_from_id(ids[idx], nb.dict()),
                            ids[idx],
                            get_connector_name_from_id(ids[idx], nb.dict()),
                            'ERROR'
                            ])
                except Exception:
                    pass

                idx += 1
    if filter == 'k8s':
        for check in hardcoded_checks:
            result_table.append([check, "Coming soon", "Coming soon", "Coming soon"])
    print("")
    print(tabulate(result_table, headers='firstrow', tablefmt='fancy_grid'))

    if failed_result_available is True:
        UNSKRIPT_GLOBALS['failed_result'] = failed_result

    print("")
    status_list_of_dict.append(status_dict)


def run_checks():
    """run_checks This function takes the filter as an argument
    and based on the filter, this function queries the DB and
    creates a temporary runnable runbooks and run them, updates
    the audit results.

    :rtype: None
    """
    parser = ArgumentParser(description='-c | --checks')
    parser.add_argument('-r',
                        '--run',
                        action='store_true',
                        help='Run options')
    parser.add_argument('--check',
                        action='store_true',
                        help=SUPPRESS)
    parser.add_argument('--script',
                        type=str,
                        nargs=1,
                        help=SUPPRESS)
    parser.add_argument('--runbook',
                        type=str,
                        nargs=1,
                        help=SUPPRESS)
    parser.add_argument('--name',
                        type=str,
                        dest='function_name',
                        help="Run an individual check")
    parser.add_argument('--all',
                        help="Run All checks available in the System",
                        action="store_true")
    parser.add_argument('--failed',
                        help="Run Failed checks again",
                        action="store_true")
    parser.add_argument('--type',
                        type=str,
                        nargs='*',
                        help='Run all checks in the given connectors')
    parser.add_argument('--report',
                        action="store_true",
                        required=False,
                        help='Report check runs')
    
    args = parser.parse_args()

    if len(sys.argv) == 2:
        parser.print_help()
        sys.exit(0)

    filter = ''
    if args.all is True:
        filter = '--all'
    elif args.failed is True:
        filter = '--failed'
    elif args.type not in ([], None):
        filter = '--type'
        largs = args.type
    elif args.function_name not in ('', None):
        filter = '--name'

    if not args:
        raise Exception("Run Checks needs filter to be specified.")


    runbooks = []
    check_list = []
    if filter == '--failed':
        run_status = get_pss_record('current_execution_status')
        exec_status = run_status.get('exec_status')
        for k, v in exec_status.items():
            if CheckOutputStatus(v.get('current_status')) == CheckOutputStatus.FAILED:
                temp_check_list = get_checks_by_connector('all', True)
                for tc in temp_check_list:
                    if tc.get('uuid') == k:
                        check_list.append(tc)
    elif filter in ('--name'):
        # If it is a `-c` option, lets get the second part of the args which
        # Will be the name of the check that need to be run and lets run it
        check_name = args.function_name
        if not check_name:
            raise Exception("Option --check should have a check name specified")
        # Lets call the db utils method to get the check by name
        check_list = get_check_by_name(check_name)
        if len(check_list) == 0:
            print(f"ERROR: Invalid Function name {check_name}")
            parser.print_help()
            print("Note: You can use TAB to autocomplete options available for the -rc --check")
            return
    elif filter == '--all':
            check_list = get_checks_by_connector("all", True)
    elif filter == '--type':
        check_list = []
        all_connectors = largs

        # Handle case when more than one connector was given with
        # comma separation but no space in between them.
        # like a,b,c
        if len(all_connectors) == 1 and ',' in  all_connectors[0]:
            all_connectors = all_connectors[0].split(',')

        for connector in all_connectors:
            connector = connector.replace(',', '')
            temp_list = get_checks_by_connector(connector.strip(), True)
            for t in temp_list:
                if t not in check_list:
                    check_list.append(t)
    else:
        parser.print_help()
        print("Note: You can use TAB to autocomplete options available for the -rc ")
        return

    if args.report:
        UNSKRIPT_GLOBALS['report'] = True

    if len(check_list) > 0:
        runbooks.append(create_jit_runbook(check_list))

    status_of_runs = []
    for rb in runbooks:
        run_ipynb(rb, status_of_runs, filter)

    update_audit_trail(status_of_runs)
    #print_run_summary(status_of_runs)
    if UNSKRIPT_GLOBALS.get('failed_result') and len(UNSKRIPT_GLOBALS.get('failed_result')):
        print("")
        print('\x1B[1;4m' + "FAILED RESULTS" + '\x1B[0m')
        print("")
        for k, v in UNSKRIPT_GLOBALS.get('failed_result').items():
            check_name = '\x1B[1;4m' + k + '\x1B[0m'
            print(check_name)
            print("Failed Objects:")
            pprint.pprint(v)
            print('\x1B[1;4m', '\x1B[0m')

    UNSKRIPT_GLOBALS['status_of_runs'] = status_of_runs

    # if UNSKRIPT_GLOBALS.get('report') is True:
    #     send_notification(status_of_runs, UNSKRIPT_GLOBALS.get('failed_result'))


def run_suites(suite_name: str):
    """run_suites This function takes the suite_name as an argument
    and queries the DB and with given UUIDs and creates a temporary
    runnable runbooks and run them, updates the audit results.

    :type suite_name: string
    :param suite_name: Suite Name string, suite name should match the
            content under `suites` section of the unskript_config.yaml

    :rtype: None
    """
    if suite_name in ("", None):
        raise Exception("Run Suite needs suite_name to be specified.")

    runbooks = []

    check_list = []
    if UNSKRIPT_GLOBALS.get('suites') and UNSKRIPT_GLOBALS.get('suites').get(suite_name):
        check_list = get_checks_by_uuid(UNSKRIPT_GLOBALS.get('suites').get(suite_name))

    if len(check_list) > 0:
        runbooks.append(create_jit_runbook(check_list))

    status_of_runs = []
    for rb in runbooks:
        run_ipynb(rb, status_of_runs)

    update_audit_trail(status_of_runs)
    print_run_summary(status_of_runs)
    if UNSKRIPT_GLOBALS.get('failed_result') and len(UNSKRIPT_GLOBALS.get('failed_result')):
        print("")
        print('\x1B[1;4m' + "FAILED RESULTS" + '\x1B[0m')
        print("")
        for k, v in UNSKRIPT_GLOBALS.get('failed_result').items():
            check_name = '\x1B[1;4m' + k + '\x1B[0m'
            print(check_name)
            print("Failed Objects:")
            pprint.pprint(v)
            print('\x1B[1;4m', '\x1B[0m')


def print_run_summary(status_list_of_dict):
    """print_run_summary This function is used to just print the Run Summary.
       :type status_list_of_dict: list
       :param status_list_of_dict: List of dictionaries that contains result of the run

       :rtype: None
    """
    all_result_table = [[TBL_HDR_CHKS_NAME, TBL_HDR_CHKS_PASS,
                         TBL_HDR_CHKS_FAIL, TBL_HDR_CHKS_ERROR]]
    summary_table = [[TBL_HDR_RBOOK_NAME, TBL_HDR_CHKS_COUNT]]
    for sd in status_list_of_dict:
        if sd == {}:
            continue
        p = f = e = s = 0
        for st in sd.get('result'):
            status = st[-1]
            check_name = st[0]
            if status == 'PASS':
                p += 1
                all_result_table.append(
                    [check_name, TBL_CELL_CONTENT_PASS, 'N/A', 'N/A'])
            elif status == 'FAIL':
                f += 1
                all_result_table.append(
                    [check_name, 'N/A', TBL_CELL_CONTENT_FAIL, 'N/A'])
            elif status == 'ERROR':
                e += 1
                all_result_table.append(
                    [check_name, 'N/A', 'N/A', TBL_CELL_CONTENT_ERROR])
            else:
                p = f = e = -1

        if UNSKRIPT_GLOBALS.get('skipped'):
            s = len(UNSKRIPT_GLOBALS.get('skipped'))

        summary_table.append([
            sd.get('runbook'),
            str(str(p) + ' / ' + str(f) + ' / ' + str(e) + ' ( ' + str(p+f+e)  + ' ) / ( ' + str(s) + ' )')
            ])

    s = '\x1B[1;20;46m' + "~~ Summary ~~" + '\x1B[0m'
    print(s)

    print(tabulate(all_result_table, headers='firstrow', tablefmt='fancy_grid'))
    print("")
    print(tabulate(summary_table, headers='firstrow', tablefmt='fancy_grid'))



def replace_input_with_globals(inputSchema: str):
    if not inputSchema:
        return None
    retval = ''
    if UNSKRIPT_GLOBALS.get('global') and len(UNSKRIPT_GLOBALS.get('global')):
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
                    if key in UNSKRIPT_GLOBALS.get('global').keys():
                        input_json_line += f"\"{key}\":  \"{key}\" ,"
        except Exception as e:
            print(f"EXCEPTION {e}")
            pass

        retval = input_json_start_line + input_json_line.rstrip(',') + '\n' + input_json_end_line

    return retval


def create_jit_runbook(check_list: list):
    """create_jit_runbook This function creates Just In Time runbook
       with just one code cell. The content will be appended with the
       task lines... and used it create the jit runbook

       :type check_list: list
       :param check_list: List of checks in the form of dictionary

       :type id: str
       :param id: Action UUID

       :rtype: None
    """
    nb = nbformat.v4.new_notebook()

    exec_id = str(uuid.uuid4())
    UNSKRIPT_GLOBALS['exec_id'] = exec_id
    failed_notebook = UNSKRIPT_EXECUTION_DIR + exec_id + '.ipynb'
    for check in check_list:
        s_connector = check.get('metadata').get('action_type')
        s_connector = s_connector.replace('LEGO', 'CONNECTOR')
        cred_name, cred_id = None, None
        for k,v in UNSKRIPT_GLOBALS.get('default_credentials').items():
            if k == s_connector:
                cred_name, cred_id = v.get('name'), v.get('id')
                break

        # No point proceeding further if the Credential is incomplete
        if cred_name is None or cred_id is None:
            #print('\x1B[1;20;46m' + f"~~ Skipping {check.get('name')} As {cred_name} Credential is Not Active ~~" + '\x1B[0m')
            if UNSKRIPT_GLOBALS.get('skipped') is None:
                UNSKRIPT_GLOBALS['skipped'] = []
            UNSKRIPT_GLOBALS['skipped'].append([check.get('name'), s_connector])
            continue


        task_lines = '''
task.configure(printOutput=True)
task.configure(credentialsJson=\'\'\'{
        \"credential_name\":''' + f" \"{cred_name}\"" + ''',
        \"credential_type\":''' + f" \"{s_connector}\"" + '''}\'\'\')
        '''
        input_json = replace_input_with_globals(check.get('inputschema'))
        if input_json:
            task_lines += input_json
        try:
            c = check.get('code')
            idx = c.index("task = Task(Workflow())")
            if c[idx+1].startswith("task.configure(credentialsJson"):
                # With credential caching now packged in, we need to
                # Skip the credential line and let the normal credential
                # logic work.
                c = c[:idx+1] + task_lines.split('\n') + c[idx+2:]
            else:
                c = c[:idx+1] + task_lines.split('\n') + c[idx+1:]
            check['code'] = []
            for line in c[:]:
                check['code'].append(str(line + "\n"))

            check['metadata']['action_uuid'] = check['uuid']
            check['metadata']['name'] = check['name']
            cc = nbformat.v4.new_code_cell(check.get('code'))
            for k, v in check.items():
                if k != 'code':
                    cc[k] = check[k]
            nb['cells'].append(cc)

        except Exception as e:
            raise e
    # The Recent Version of Docker, the unskript-ctl spews a lot of errors like this:
    #
    # ERROR:traitlets:Notebook JSON is invalid: Additional properties are not allowed ('orderProperties', 'description',
    # 'version', 'name', 'inputschema', 'uuid', 'tags', 'type', 'language' were unexpected)
    # This Failed validating 'additionalProperties' in code_cell:
    #
    # This is because the nbformat.write() complains about unknown attributes that are present
    # in the IPYNB file. We dont need these attributes when we run the notebook via the Command Line.
    # So we surgically eliminate these keys from the NB dictionary.
    unknown_attrs = ['description', 'uuid', 'name', 'type', 'inputschema', 'version', 'orderProperties', 'tags', 'language']
    for cell in nb.get('cells'):
        if cell.get('cell_type') == "code":
            # This check is needed because the ID value is by default saved
            # as integer in our code-snippets to enable drag-and-drop
            cell['id'] = str(cell.get('id'))
        for attr in unknown_attrs:
            del cell[attr]
    nbformat.write(nb, failed_notebook)


    return failed_notebook




def update_audit_trail(status_dict_list: list):
    """update_audit_trail This function will update the status of each run of the runbook

       :type status_dict_list: list
       :param status_dict: List of Python Dictionary that has the status for all the checks that
             were run for the given runbook run

       :rtype: None
    """
    global UNSKRIPT_GLOBALS
    trail_data = {}
    id = ''
    try:
        get_pss_record('audit_trail')
    except Exception:
        pass
    finally:
        k = str(datetime.now())
        p = f = e = 0
        if UNSKRIPT_GLOBALS.get('exec_id') is None:
            id = uuid.uuid4()
        else:
            id = UNSKRIPT_GLOBALS.get('exec_id')
        trail_data = {}
        trail_data[id] = {}
        trail_data[id]['time_stamp'] = k
        trail_data[id]['runbook'] = id + '_output.ipynb'
        trail_data[id]['check_status'] = {}
        for sd in status_dict_list:
            if sd == {}:
                continue
            for s in sd.get('result'):
                check_name, check_id, connector, status = s
                if status == 'PASS':
                    p += 1
                elif status == 'FAIL':
                    f += 1
                elif status == 'ERROR':
                    e += 1
                trail_data[id]['check_status'][check_id] = {}
                trail_data[id]['check_status'][check_id]['check_name'] = check_name
                trail_data[id]['check_status'][check_id]['status'] = status
                trail_data[id]['check_status'][check_id]['connector'] = connector
                if UNSKRIPT_GLOBALS.get('failed_result'):
                    c_name = connector + ':' + check_name 
                    for name, obj in UNSKRIPT_GLOBALS.get('failed_result').items():
                        if name in (c_name, check_name):
                            trail_data[id]['check_status'][check_id]['failed_objects'] = obj

        trail_data[id]['summary'] = f"Summary (total/p/f/e): {p+e+f}/{p}/{f}/{e}"
    upsert_pss_record('audit_trail', trail_data)
    return id

def format_size(size_bytes):
    # Define the size units
    size_units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

    # Find the appropriate unit
    index = 0
    while size_bytes >= 1024 and index < len(size_units) - 1:
        size_bytes /= 1024
        index += 1

    return f"{size_bytes:.2f} {size_units[index]}"



def read_ipynb(filename: str) -> nbformat.NotebookNode:
    """read_ipynb This function takes the Runbook name and reads the content
           using nbformat.read, Reads as Version 4.0 and returns the
           notebooknode.

       :type filename: str
       :param filename: Runbook name

       :rtype: NotebookNode
    """
    nb = None
    if os.path.exists(filename) is not True:
        print(f"File {filename} does not exists!")
        return nb

    try:
        with open(filename, 'r') as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        raise e

    return nb


def get_code_cell_action_uuids(content: dict) -> list:
    """get_code_cell_action_uuids This function takes in the notenode dictionary
           iterates over it to find all the Action UUIds for the code-cells and
           returns it as a list

       :type content: dict
       :param content: Notebook Node Dictionary

       :rtype: List of Action UUIDs
    """
    retval = []
    if content in ('', None):
        print("Content sent is empty")
        return retval

    for cell in content.get('cells'):
        if cell.get('cell_type') == 'code':
            if cell.get('metadata').get('tags') is not None:
                tags = None
                if (isinstance(cell.get('metadata').get('tags'), list)) is True:
                    if len(cell.get('metadata').get('tags')) != 0:
                        tags = cell.get('metadata').get('tags')[0]
                else:
                    tags = None

                if "unSkript:nbParam" != tags:
                    if cell.get('metadata').get('action_uuid') is not None:
                        retval.append(cell.get('metadata').get('action_uuid'))
            else:
                if cell.get('metadata').get('action_uuid') is not None:
                    retval.append(cell.get('metadata').get('action_uuid'))

    return retval

def get_last_code_cell_output(content: dict) -> list:
    """get_last_code_cell_output This function takes in the notebook node dictionary
           finds out the last cell output and returns in the form of a dict

       :type content: dict
       :param content: NotebookNode as Dictionary

       :rtype: Last output in the form of Python list
    """
    retval = []
    if content in ('', None):
        print("Content sent is empty")
        return retval

    for cell in content.get('cells'):
        if cell.get('cell_type') == 'code':
            if cell.get('id') == 'lastcell':
                retval = cell.get('outputs')
    print("")
    return retval


def get_action_name_from_id(action_uuid: str, content: dict) -> str:
    """get_action_name_from_id This function takes in the action_uuid as string
           and notebook node as dictionary. Iterates over the dictionary for code cells
           matches the action_uuid against the given uuid, if match found, returns
           the name of the the Action that matches the UUIDs.

       :type action_uuid: str
       :parm action_uuid: Action UUID as a String

       :type content: dict
       :param content: Notenode as Dictionary

       :rtype: Name of the Action that matches the given UUID, returns as string
    """
    retval = ''
    if content in ('', None):
        return retval

    for cell in content.get('cells'):
        if cell.get('metadata').get('action_uuid') == action_uuid:
            retval = cell.get('metadata').get('name')

    return retval


def get_connector_name_from_id(action_uuid: str, content: dict) -> str:
    """get_connector_name_from_id This function takes in the action_uuid as string
       and notebook node as dictionary. Iterates over the dictionary for code cells
       that match the action_uuid and returns the action_type (connector_type).

       :type action_uuid: string
       :param action_uuid: Action UUID

       :type content: dict
       :param content: Notebooknode as Dictionary

       :rtype: string: Name of the connector that matches the given UUID.
    """
    retval = ''
    if content in ('', None):
        return retval
    for cell in content.get('cells'):
        if cell.get('metadata').get('action_uuid') == action_uuid:
            if cell.get('metadata').get('action_type') is not None:
                retval = cell.get('metadata').get(
                    'action_type').replace('LEGO_TYPE_', '').lower()

    return retval


def create_creds_mapping():
    """create_creds_mapping This function creates a mapping based on the Credential TYPE, 
       the mapping would be a list of dictionaries with {"name", "id"}

       :rtype: None
    """
    global UNSKRIPT_GLOBALS
    creds_files = os.environ.get('HOME').strip('"') + CREDENTIAL_DIR + '/*.json'
    list_of_creds = glob.glob(creds_files)
    d = {}
    for creds in list_of_creds:
        with open(creds, 'r') as f:
            c_data = json.load(f)
            if c_data.get('metadata').get('connectorData') == "{}":
                continue
            d[c_data.get('metadata').get('type')] = {"name": c_data.get('metadata').get('name'),
                  "id": c_data.get('id')}
    UNSKRIPT_GLOBALS['default_credentials'] = d


def print_runbook_params(properties: dict, required: list, orderInputParameters: list = []):
    """print_runbook_params This function prints the parameterSchema. It respects OrderInputParameters
       and lists the Parameters in the same order as displayed in OrderInputParameters.

       :type properties: dict
       :param properties: Properties metadata read from the Runbook

       :type required: list
       :param required: List of required parameters read from the Runbook

       :type orderInputParameters: list
       :param orderInputParameters: Order in which the parameters should be shown

       :rtype: None
    """
    if not properties:
        return

    print("\033[1m Expected Parameters to run the Runbook \033[0m")
    param_data = [['\033[1m Name \033[0m',
                   '\033[1m Type \033[0m',
                   '\033[1m Description \033[0m',
                   '\033[1m Default \033[0m']]
    prop_data = {}
    if not orderInputParameters:
        prop_data = properties
    else:
        # Starting python version 3.6 and above dict are required to retain the order in which they
        # are inserted. So Storing in prop_data the same way as orderInputParameters would retain it.
        for _param in orderInputParameters:
            prop_data[_param] = properties.get(_param)

    for k, v in prop_data.items():
        if k in required:
            k = '\033[1m' + k + '*' + '\033[0m'
        param_type = v.get('type')
        if v.get('enum') is not None:
            param_type = "enum"
            param_type = param_type + "\n" + \
                str(v.get('enum')).replace(',', ' |')
        # Some beautification, if description has 4 or
        # more continuous whitespace lets replace it with a newline
        # If not below command just copies the content of description to text
        text = re.sub(r"\s{4,}", "\n", v.get('description'))
        param_data.append([k,
                           param_type,
                           text,
                           v.get('default') or 'No Default Value'
                           ])
    print(tabulate(param_data, headers='firstrow', tablefmt='fancy_grid'))
    print("* Required")


def get_runbook_metadata_contents(_runbook) -> dict:
    """get_runbook_metadata_contents This function takes Runbook name as
    the input, reads the metadata content
       of the Runbook and returns the content of the runbook in the form of
       python Dictionary.

       :type _runbook: str
       :param _runbook: Runbook Name as a string

       :rtype: Python dictionary of the Metadata of the runbook.
    """
    if not _runbook:
        return {}

    _runbook_contents = {}
    file_name_to_read = ''
    if not _runbook.endswith('.ipynb'):
        _runbook = _runbook + '.ipynb'

    if os.environ.get('RUNBOOK_PATH'):
        if os.path.exists(os.environ.get('RUNBOOK_PATH') + '/' + _runbook):
            file_name_to_read = os.environ.get('RUNBOOK_PATH') + '/' + _runbook
    else:
        l = glob.glob(os.environ.get('HOME') + '/runbooks/*/' + _runbook)
        if not l:
            # If runbook was not found in $HOME/runbooks/*/ then search in $HOME/runbooks
            l = glob.glob(os.environ.get('HOME') + '/runbooks/' + _runbook)
        if l:
            if os.path.exists(l[0]):
                file_name_to_read = l[0]
        else:
            if os.path.exists(os.environ.get('PWD') + '/' + _runbook):
                file_name_to_read = os.environ.get('PWD') + '/' + _runbook

    if os.path.exists(_runbook) is True:
        file_name_to_read = _runbook

    if not file_name_to_read:
        raise Exception(f"Runbook Not found {_runbook}")

    if file_name_to_read:
        with open(file_name_to_read, 'r') as f:
            _runbook_contents = json.loads(f.read())

    _runbook_contents['runbook_name'] = file_name_to_read
    return _runbook_contents


def non_interactive_parse_runbook_param(args) -> dict:
    """non_interactive_parse_runbook_param This function is called when
    --runbook_parmas are sent when running the runbook.

       :type args: list
       :param args: Python List the arguments that were passed with the
       `-rr` option from command line.

       :rtype: Python Dictionary of the Runbook Parameters with values and the Runbookname
    """
    # The syntax for running runbook would be
    # unskript-ctl.sh -rr <RUNBOOK_NAME> [-runbook_param1 value1] [-runbook_param2 value2]

    if not args:
        return {}

    retval = {}
    retval['params'] = {}
    if args[0] in ('-h', '--h'):
        sys.exit(0)

    _runbook_contents = get_runbook_metadata_contents(args[0])
    retval['runbook_name'] = _runbook_contents.get('runbook_name')

    mdata = _runbook_contents.get('metadata')
    if mdata:
        if not mdata.get('parameterSchema'):
            # This means there is no Runbook parameter defined, return empty dictionary
            print("\033[1m No Runbook Parameters required \033[0m")
            s = [x for x in args if x in ('-h', '--h')]
            if s:
                parser.print_help()
                sys.exit(0)
            return {}

        properties = mdata.get('parameterSchema').get('properties')
        required = mdata.get('parameterSchema').get('required')
        # When we have the orderInputParameters implemented we need to read it
        # in from metadata of runbook.
        orderInputParameters = []
        arg_list = args[1:]
        if len(properties.keys()):
            # FIXME: If properties.type is secretstring or password, how do we
            # take that input from user?
            if len(arg_list) < len(required) * 2:
                print_runbook_params(
                    properties=properties,
                    required=required,
                    orderInputParameters=orderInputParameters
                    )
                return {}
        else:
            print("\033[1m No Runbook Parameters required  \033[0m")
            s = [x for x in args if x in ('-h', '--h')]
            if s:
                parser.print_help()
                sys.exit(0)
            return retval
        values = []
        keys = []
        for idx,k in enumerate(arg_list):
            if k in ('-h', '--h'):
                print_runbook_params(
                    properties=properties,
                    required=required,
                    orderInputParameters=orderInputParameters
                    )
                return {}

            if (idx+1) % 2 == 0:
                values.append(k)
                continue
            k = k.strip('--')
            if k not in properties.keys():
                print_runbook_params(
                    properties=properties,
                    required=required,
                    orderInputParameters=orderInputParameters
                    )
                print(f"\033[1m Runbook Parameter name does not match: '{k}' \
                      Does not match any parameter name. Available Values are \
                      {list(properties.keys())} \033[0m")
                return {}
            keys.append(k)
        if len(values) != len(keys):
            print_runbook_params(
                properties=properties,
                required=required,
                orderInputParameters=orderInputParameters
                )
            return {}

        for i, val in enumerate(values):
            retval['params'][keys[i]] = val

        return retval
    raise Exception("Unable to Parse Runbook file, No Metadata present in the given runbook")


def interactive_parse_runbook_param(args) -> dict:
    """interactive_parse_runbook_param This function is called when -rr is called with the Runbook
       that needs parameters to run the runbook.

       :type args: list
       :param args: Python List the arguments that were passed with the `-rr`
       option from command line.

       :rtype: Python Dictionary of the Runbook Parameters with values and the Runbookname
    """
    # The syntax for interactive running would be like this -
    # unskript-ctl.sh --rr <RUNBOOK>
    if not args:
        return {}

    retval = {}
    retval['params'] = {}
    if args[0] in ('-h', '--h'):
        parser.print_help()
        sys.exit(0)

    _runbook_contents = get_runbook_metadata_contents(args[0])
    retval['runbook_name'] = _runbook_contents.get('runbook_name')

    mdata = _runbook_contents.get('metadata')
    if mdata:
        if not mdata.get('parameterSchema'):
            # This means there is no Runbook parameter defined, return empty dictionary
            print("\033[1m No Runbook Parameters required \033[0m")
            return retval

        properties = mdata.get('parameterSchema').get('properties')
        required = mdata.get('parameterSchema').get('required')

        all_param_names = list(properties.keys())
        optional_params = []
        try:
            optional_params = set(all_param_names.sort()) - set(required.sort())
        except Exception:
            if not required:
                optional_params = all_param_names

        for param in required:
            retval['params'][param] = input(("Input the Value or \033[1m  "
                                            f"{param} \033[0m (Required): "))
        for o_param in optional_params:
            default_string = ""
            if properties.get(o_param).get('default') is not None:
                default_string = fr"Defualt value: \033[1m \{properties.get(o_param).get('default')} \033[0m"
            temp = input(fr" Input the Value for \033[1m {o_param} \033[0m \(OPTIONAL, {default_string} Hit enter to use default): ")
            if not temp.strip():
                if properties.get(o_param).get('default') is not None:
                    retval['params'][o_param] = properties.get(o_param).get('default')
                continue
            retval['params'][o_param] = temp

        return retval
    raise Exception("Unable to Parse Runbook, No Metadata present in the given runbook")


def parse_runbook_param(args):
    """parse_runbook_param This function is called when -rr Option is used in the command line

       :type args: list
       :param args: Arguments that was passed with the -rr option as a python list

       :rtype: None
    """
    if not args:
        return

    if len(args) == 1:
        retval = interactive_parse_runbook_param(args)
    elif len(args) >= 2:
        retval = non_interactive_parse_runbook_param(args)

    if retval:
        if retval.get('params') is not None:
            os.environ['ACA_RUNBOOK_PARAMS'] = json.dumps(retval.get('params'))
        if retval.get('runbook_name') is not None:
            status_of_run = []
            run_ipynb(retval.get('runbook_name'), status_of_run)
            exec_id = update_audit_trail(status_of_run)
            status_list = status_of_run[0].get('result')
            es = {}
            exec_id = str(exec_id)
            es['exec_status'] = {}
            es['exec_status'][exec_id] = {}
            run_command_string = retval.get(
                'runbook_name') + '\n' + "Runbook Parameters: " + str(args[1:])
            es['exec_status'][exec_id]['failed_runbook'] = run_command_string
            es['exec_status'][exec_id]['check_name'] = "RUNBOOK"
            if status_list[0][-1] == "FAIL":
                f = 2
            elif status_list[0][-1] == "PASS":
                f = 1
            es['exec_status'][exec_id]['current_status'] = CheckOutputStatus(f)
            es['exec_status'][exec_id]['connector_type'] = "RUNBOOK"

            upsert_pss_record('current_execution_status', es)

    return

def parse_creds(args):
    """parse_creds parses the given arguments. Currently only
       file based credential creation is supported via command options.
       (K8S). For the rest of credentials, UI is prompted.

       :type args: list
       :param args: ParseArgs List that it returns for the given option

       :rtype: None
    """
    # Check if creds that need to be created is for k8s, if yes
    # read the given kubecofnig and create the credential of it.
    parser = ArgumentParser(description='-cc | --create-credentials')
    parser.add_argument('-cc',
                        '--create-credentials',
                        help=SUPPRESS,
                        required=True,
                        default=True,
                        action='store_true')
    parser.add_argument('--type',
                        dest='connector_type',
                        type=str,
                        nargs=REMAINDER,
                        help='Type of connector to be created')

    args = parser.parse_args()

    if args.connector_type in ('', None):
        display_creds_ui()
        return

    largs = args.connector_type
    connector_type = largs[0]
    connector_type = connector_type.replace('-','')

    if connector_type.lower() in ("k8s", "kubernetes"):
        if len(largs) == 1:
            print("ERROR: Need a path for kubeconfig file as value for the k8s credential")
            parser.print_help()
            sys.exit(1)
        if os.path.exists(largs[-1]) is False:
            print(f"ERROR: Credential File {args[1]} does not exist, please check path")
            parser.print_help()
            sys.exit(1)
        with open(largs[-1], 'r', encoding='utf-8') as f:
            creds_data = f.read()
        k8s_creds_file = os.environ.get('HOME') + CREDENTIAL_DIR + '/k8screds.json'
        with open(k8s_creds_file, 'r', encoding='utf-8') as f:
            k8s_creds_content = json.loads(f.read())
        try:
            k8s_creds_content['metadata']['connectorData'] = json.dumps({"kubeconfig": creds_data})
            with open(k8s_creds_file, 'w', encoding='utf-8') as f:
                f.write(json.dumps(k8s_creds_content, indent=2))
        except:
            print(f"ERROR: Updating K8S Credential. Please check if kubeconfig file exists")
            sys.exit(1)
        finally:
            print("Successfully Created K8S Credential")

    else:
        # Currently only file based creds creation is supported,
        # for the rest, display UI.
        display_creds_ui()

def display_creds_ui():
    """display_creds_ui Display the npyscreen based UI for user to add creds
    """
    try:
        from creds_ui import main as ui
        ui()
    except:
        print("Required Python library creds_ui is not packaged, please raise an issue on Github")



def save_check_names(filename: str):
    """save_check_names queries ZoDB Database and finds out all checks available and
       dumps it to the filename given as argument

       :type filename: String
       :param filename: filename to which the output should be written
    """
    if not filename:
        return

    list_of_names = get_all_check_names()
    with open(filename, 'w', encoding='utf-8') as f:
        for name in list_of_names:
            f.write(name + '\n')


def run_script(script:list[str]):
    """run_script: This function does the following:
    - Run the provided script
    - Creates a directory where all the output will be saved.
    - Stores the output of the script in a file
    - Creates a json for the run, containing some metadata about the script.
    """
    parser = ArgumentParser(description='--run-script')
    parser.add_argument('-r',
                        '--run',
                        required=True,
                        default=True,
                        help=SUPPRESS,
                        action="store_true")
    parser.add_argument('--report',
                        help="Report script run",
                        required=False,
                        action="store_true")
    parser.add_argument('--check',
                        nargs='*',
                        help=SUPPRESS)
    parser.add_argument('--script',
                        help="Script to be run",
                        nargs='*')

    # Parse Arguments
    args, _ = parser.parse_known_args()

    if len(sys.argv) == 2:
        parser.print_help()
        sys.exit(0)

    script = args.script
    if len(args.script) == 0:
        parser.print_help()
        sys.exit(0)

    # Do the basic sanity check like file exists and has required permission
    if not os.path.exists(script[0]):
        print(f'''
            {bcolors.FAIL}{script[0]} does not exist. Please ensure that you
            provide the full path. {bcolors.ENDC}
            ''')
        return

    accessmode = os.F_OK | os.X_OK
    if not os.access(script[0], accessmode):
        print(f'{bcolors.FAIL}{script[0]} is not executable. {bcolors.ENDC}')
        return

    if not UNSKRIPT_GLOBALS.get('CURRENT_EXECUTION_RUN_DIRECTORY'):
        # Use the first command as the prefix for the file name.
        # if it contains /, use the last entry
        # output_prefix = script[0].split('/')[-1]
        # output_dir = create_execution_run_directory(output_prefix)
        output_dir = create_execution_run_directory()
    else:
        output_dir = UNSKRIPT_GLOBALS.get('CURRENT_EXECUTION_RUN_DIRECTORY')

    output_file = UNSKRIPT_SCRIPT_RUN_OUTPUT_FILE_NAME
    output_file_txt = output_dir + "/" + output_file + ".txt"
    output_file_json = output_dir + "/" + output_file + ".json"

    # We need to export an env variable, so that the scripts can put their
    # output in that directory.
    current_env = os.environ.copy()
    current_env[UNSKRIPT_SCRIPT_RUN_OUTPUT_DIR_ENV] = output_dir

    script_to_print = ' '.join(script)
    print(f'{bcolors.OKGREEN}Executing script {script_to_print}{bcolors.ENDC}')
    print(f'{bcolors.OKBLUE}OUTPUT FILE: {output_file_txt}{bcolors.ENDC}')
    st = time.time()
    status = "SUCCESS"
    error = None
    try:
        with open(output_file_txt, "w") as f:
            result = subprocess.run(script,
                                    check=True,
                                    env=current_env,
                                    stdout=f,
                                    stderr=f)
    except Exception as e:
        print(f'{bcolors.FAIL}{" ".join(script)} failed, {e}{bcolors.ENDC}')
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
        with open(output_file_json, "w") as f:
            json.dump(json_output, fp=f)

        # if args.report:
        #     send_notification(None, None, output_metadata_file=output_file_json)
    except Exception as e:
        print(f'{bcolors.FAIL} output file creation failed, {e}{bcolors.ENDC}')
        sys.exit(0)


def run_main():
    parser = ArgumentParser()

    parser.add_argument('-r',
                        '--run',
                        help='Run Options',
                        action="store_true")
    parser.add_argument('--script',
                        help='Run script',
                        nargs=1)
    parser.add_argument('--runbook',
                        type=str,
                        nargs='*',
                        help='Run the given runbook FILENAME [-RUNBOOK_PARM1 VALUE1] etc..')
    parser.add_argument('--check',
                        help='Run checks',
                        type=str,
                        nargs='*')
    parser.add_argument('--report',
                        help="Report results",
                        action='store_true')
    

    args,additional_args = parser.parse_known_args()
    if len(additional_args) > 0:
        args.check = additional_args
    if len(sys.argv) <= 2:
        parser.print_help()
        sys.exit(1)
    
    if args.check not in ('', None):
        run_checks()

    if args.runbook not in ('', None):
        if len(args.runbook) == 0:
            parser.print_help()
            sys.exit(0)
        else:
            # TBD: Dynamic Parser
            parse_runbook_param(args.runbook)

    if args.script not in ('', None):
        run_script(args.script)

    if UNSKRIPT_GLOBALS.get('report') is True or args.report is True:
        output_dir = create_execution_run_directory()
        summary_result = None
        failed_objects = None
        if args.check:
            summary_result = UNSKRIPT_GLOBALS.get('status_of_runs')
            failed_objects = UNSKRIPT_GLOBALS.get('failed_result')
            output_json_file = None
        if args.script:
            output_json_file = output_dir + '/' + UNSKRIPT_SCRIPT_RUN_OUTPUT_FILE_NAME + '.json'
        
        send_notification(summary_result_table=summary_result,
                          failed_result=failed_objects,
                          output_metadata_file=output_json_file)


if __name__ == "__main__":
    try:
        load_or_create_global_configuration()
        create_creds_mapping()
    except Exception as error:
        raise error

    parser = ArgumentParser(prog='unskript-ctl')

    version_number = "0.1.0"
    description = ""
    description = description + str("\n")
    description = description + str("\t  Welcome to unSkript CLI Interface \n")
    description = description + str(f"\t\t   VERSION: {version_number} \n")
    parser.description = description

    parser.add_argument('-l',
                        '--list',
                        dest="list_option",
                        type=str,
                        nargs=REMAINDER,
                        help="List Options")

    parser.add_argument('-r',
                        '--run',
                        dest="run_option",
                        type=str,
                        nargs=REMAINDER,
                        help="Run Options")
    
    parser.add_argument('-s',
                        '--show',
                        dest="show_option",
                        type=str,
                        nargs=REMAINDER,
                        help='Show Options')
    
    parser.add_argument('-d',
                        '--debug',
                        dest="debug_option",
                        type=str,
                        nargs=REMAINDER,
                        help='Debug Options')
    
    parser.add_argument('--create-credential',
                        type=str,
                        nargs=REMAINDER,
                        help='Create Credential [-creds-type creds_file_path]')
    
    args = parser.parse_args()

    if len(sys.argv) <= 2:
        parser.print_help()
        sys.exit(0)

    if args.list_option not in ('', None):
        list_main()
    elif args.run_option not in ('', None):
        run_main()
    elif args.show_option not in ('', None):
        show_main() 
    elif args.debug_option not in ('', None):
        debug_session_main()
    elif args.create_credential not in ('', None):
        if len(args.create_credential) == 0:
            display_creds_ui()
        else:
            parse_creds(args.create_credential)
    else:
        parser.print_help()
