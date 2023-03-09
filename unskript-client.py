#!/usr/bin/env python
#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE
#
#
import argparse
import os
import nbformat
import sys
import glob
import json
import nbformat
import pprint
import yaml
import re
import uuid 

from tabulate import tabulate
from datetime import datetime 
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
from unskript.legos.utils import CheckOutput, CheckOutputStatus
from db_utils import *

import ZODB, ZODB.FileStorage
from ZODB import DB

"""
This python client can be used to
1. List all available runbooks
2. Run the Runbook and prints out result of the execution

Note:
This program assumes the following
* The Runbooks are located in $HOME/runbooks folder
  This assumption is valid for unSkript docker use-case.
* This script assumes the system has all the python dependent libraries
  installed before using this script.
"""

"""
LIST OF CONSTANTS USED IN THIS FILE
"""
GLOBAL_CONFIG_PATH="/data/unskript_config.yaml"
CREDENTIAL_DIR="/.local/share/jupyter/metadata/credential-save"
ZODB_DB_PATH="/var/unskript/snippets.db"
TBL_HDR_CHKS_NAME="\033[36m Checks Name \033[0m"
TBL_HDR_CHKS_PASS="\033[32m Passed Checks \033[0m"
TBL_HDR_CHKS_FAIL="\033[35m Failed Checks \033[0m"
TBL_HDR_CHKS_ERROR="\033[31m Errored Checks \033[0m"
TBL_HDR_RBOOK_NAME="\033[36m Runbook Name \033[0m"
TBL_HDR_CHKS_COUNT="\033[32m Checks Count (Pass/Fail/Error) (Total checks) \033[0m"
TBL_CELL_CONTENT_PASS="\033[1m PASS \033[0m"
TBL_CELL_CONTENT_FAIL="\033[1m FAIL \033[0m"
TBL_CELL_CONTENT_ERROR="\033[1m ERROR \033[0m"
TBL_HDR_DSPL_CHKS_NAME="\033[35m Failed Check Name / TS \033[0m"
TBL_HDR_DSPL_CHKS_UUID="\033[1m Failed Check UUID \033[0m"
TBL_HDR_CHKS_UUID="\033[1m Check UUID \033[0m"
TBL_HDR_LIST_CHKS_CONNECTOR="\033[36m Connector Name \033[0m"



def load_or_create_global_configuration():
    """load_global_configuration This function reads the unskript_config.yaml file from /data
       and sets os.env variables which we shall use it in the subsequent functions.
       :rpath: None
    """
    global_content = {}
    if os.path.exists(GLOBAL_CONFIG_PATH) == True:
        # READ EXISTING FILE AND SET ENV VARIABLES
        with open(GLOBAL_CONFIG_PATH, 'r') as f:
            global_content = yaml.safe_load(f)

    
    for k,v in global_content.items():
        k = k.upper()
        os.environ[k] = json.dumps(v)


def insert_first_and_last_cell(nb: nbformat.NotebookNode) -> nbformat.NotebookNode:
    """insert_first_and_last_cell This function inserts the first cell (unskript internal)
           and the last cell to a given notebook and returns the NotebookNode object back.

       :type nb: NotebookNode 
       :param nb: NotebookNode Object that has the runbook content in it

       :rtype: NotebookNode that has the first and the last cell inserted in it
    """
    if nb is None:
        return 
    ids = get_code_cell_action_uuids(nb.dict())
    # Firstcell content. Here the workflow will take the UUIDS that we got from
    # get_code_cell_action_uuids

    #FIXME: NEED TO CREATE FIRST CELL VARIABLES BASED ON ENV VARIABLE SET IN THE CONFIG FILE
    
    first_cell_content = f'''\
import json
from unskript import nbparams
from unskript.fwk.workflow import Task, Workflow
from unskript.secrets import ENV_MODE, ENV_MODE_LOCAL

env = {{"ENV_MODE": "ENV_MODE_LOCAL"}}
secret_store_cfg = {{"SECRET_STORE_TYPE": "SECRET_STORE_TYPE_LOCAL"}}

paramDict = {{}}
paramsJson = json.dumps(paramDict)
nbParamsObj = nbparams.NBParams(paramsJson)
w = Workflow(env, secret_store_cfg, None, global_vars=globals(), check_uuids={ids})'''


    # Firstcell content. This is a static content
    last_cell_content = f'''\
from unskript.legos.utils import CheckOutput, CheckOutputStatus


try:
    if 'w' in globals():
        if w.check_run:
            for id,output in w.check_output.items():
                output = json.loads(output)
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
        print("ERROR: Runbook seems empty, nothing to run")
        return nb
    
    if cells[0].get('cell_type') == 'code':
        tags = None 
        if cells[0].get('metadata').get('tags') != None:
            if len(cells[0].get('metadata').get('tags')) != 0:
                tags = cells[0].get('metadata').get('tags')[0]

        # If we have the first cell present, remove it before inserting the new one
        if "unSkript:nbParam" == tags:
            nb['cells'].remove(nb['cells'][0])
    
    # First Cell insertion
    nb['cells'].insert(0, nbformat.v4.new_code_cell(first_cell_content, id='firstcell'))
    # Last Cell insertion
    nb['cells'].extend([nbformat.v4.new_code_cell(last_cell_content, id='lastcell')])
    
    return nb


# These are all trigger functions that are
# called based on argument passed
def list_runbooks():
    """list_runbooks  This is simple routine that uses python glob to fetch
            the list of runbooks stored in the a predefined path ~/runbooks
            and prints the available runbook and prints in a tabular form.
    
    """
    runbooks = glob.glob(os.environ.get('HOME') + '/runbooks/*.ipynb')
    runbooks += glob.glob(os.environ.get('HOME') + '/runbooks/*/*.ipynb')

    runbooks.sort()
    table = [["Runbook Name",  "File Name"]]
    for runbook in runbooks:
        contents = {}
        with open(runbook, 'r') as f:
            contents = f.read()
        try:
            contents = json.loads(contents)
            name = contents.get('metadata').get('execution_data').get('runbook_name')
            filename = os.path.basename(runbook)
            table.append([name,  filename])
        except Exception as e:
            pass

    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

def run_ipynb(filename: str, status_list_of_dict: list = []):
    """run_ipynb This function takes the Runbook name and executes it
           using nbclient.execute()

       :type filename: str 
       :param filename: Runbook name

       :rtype: None, Runbook execution will be displayed
    """
    nb = read_ipynb(filename)
   
    # We store the Status of runbook execution in status_dict
    status_dict = {}
    status_dict['runbook'] = filename
    status_dict['result'] = []
    r_name = '\x1B[1;20;42m' + "Executing Runbook -> " + filename.strip() + '\x1B[0m'
    print(r_name)

    if nb == None: 
        raise Exception("Unable to Run the Ipynb file, internal service error")
    
    nb = insert_first_and_last_cell(nb)

    client = NotebookClient(nb=nb, kernel_name="python3")

    try:
        client.execute()
    except CellExecutionError as e:
        raise e
    finally:
        nbformat.write(nb, "/tmp/output.ipynb")
        new_nb = None
        with open("/tmp/output.ipynb", "r") as f:
            new_nb = nbformat.read(f, as_version=4)
        outputs = get_last_code_cell_output(new_nb.dict())
    
    ids = get_code_cell_action_uuids(nb.dict())
    result_table = [["Checks Name", "Result", "Failed Count", "Error"]]
    if len(outputs) == 0:
        raise Exception("Unable to execute Runbook. Last cell content is empty")

    results = outputs[0]
    idx = 0
    r = results.get('text')
    failed_result_available = False
    failed_result = {}

    for result in r.split('\n'):
        if result == '':
            continue
        payload = json.loads(result)
        
        try:
            if CheckOutputStatus(payload.get('status')) == CheckOutputStatus.SUCCESS:
                result_table.append([get_action_name_from_id(ids[idx], nb.dict()), TBL_CELL_CONTENT_PASS, 0, 'N/A'])
                status_dict['result'].append([get_action_name_from_id(ids[idx], nb.dict()), ids[idx], get_connector_name_from_id(ids[idx], nb.dict()), 'PASS'])
            elif CheckOutputStatus(payload.get('status')) == CheckOutputStatus.FAILED: 
                failed_objects = payload.get('objects')
                failed_result[get_action_name_from_id(ids[idx], nb.dict())] = failed_objects 
                result_table.append([get_action_name_from_id(ids[idx], nb.dict()), TBL_CELL_CONTENT_FAIL, len(failed_objects), 'N/A'])
                failed_result_available = True
                status_dict['result'].append([get_action_name_from_id(ids[idx], nb.dict()), ids[idx], get_connector_name_from_id(ids[idx], nb.dict()), 'FAIL'])
            elif CheckOutputStatus(payload.get('status')) == CheckOutputStatus.RUN_EXCEPTION:
                result_table.append([get_action_name_from_id(ids[idx], nb.dict()), TBL_CELL_CONTENT_ERROR, 0, payload.get('error')])
                status_dict['result'].append([get_action_name_from_id(ids[idx], nb.dict()), ids[idx], get_connector_name_from_id(ids[idx], nb.dict()), 'ERROR'])
        except Exception as e:
            pass
        update_current_execution(payload.get('status'), ids[idx], nb.dict())
        update_check_run_trail(ids[idx], 
                           get_action_name_from_id(ids[idx], nb.dict()),
                           get_connector_name_from_id(ids[idx], nb.dict()),
                           CheckOutputStatus(payload.get('status')), 
                           failed_result)
        idx += 1

    # New Line to make the output clear to see
    print("")
    print(tabulate(result_table, headers='firstrow', tablefmt='fancy_grid'))
    
    if failed_result_available == True:
        print("")
        print("FAILED RESULTS")
        for k,v in failed_result.items():
            check_name = '\x1B[1;4m' + k + '\x1B[0m'
            print(check_name) 
            print("Failed Objects:")
            pprint.pprint(v)
            print('\x1B[1;4m', '\x1B[0m')
    
    print("")
    status_list_of_dict.append(status_dict)


def run_checks(filter: str):
    """run_checks This function takes the filter as an argument
    and based on the filter, this function queries the DB and 
    creates a temporary runnable runbooks and run them, updates
    the audit results.

    :type filter: string
    :param filter: Filter string, possible values are all,<connector>,failed
    
    :rtype: None
    """
    if filter in ("", None):
        raise Exception("Run Checks needs filter to be specified.")
    
    runbooks = []
    check_list = []
    if filter == 'failed':
        run_status = get_pss_record('current_execution_status')
        exec_status = run_status.get('exec_status')
        for k,v in exec_status.items():
            if CheckOutputStatus(v.get('current_status')) == CheckOutputStatus.FAILED:
                temp_check_list = get_checks_by_connector('all', True)
                for tc in temp_check_list:
                    if tc.get('uuid') == k:
                        check_list.append(tc)
    else:
        check_list = get_checks_by_connector(filter, True)
    
    if len(check_list) > 0:
        runbooks.append(create_jit_runbook(check_list))
    
    status_of_runs = []
    for rb in runbooks:
        run_ipynb(rb, status_of_runs)

    update_audit_trail(status_of_runs)
    print_run_summary(status_of_runs)


def print_run_summary(status_list_of_dict):
    """print_run_summary This function is used to just print the Run Summary.
       :type status_list_of_dict: list 
       :param status_list_of_dict: List of dictionaries that contains result of the run

       :rtype: None
    """
    all_result_table = [[TBL_HDR_CHKS_NAME, TBL_HDR_CHKS_PASS, TBL_HDR_CHKS_FAIL, TBL_HDR_CHKS_ERROR]]
    summary_table = [[TBL_HDR_RBOOK_NAME, TBL_HDR_CHKS_COUNT]]
    for sd in status_list_of_dict:
        if sd == {}:
            continue
        p = f = e = 0
        for st in sd.get('result'):
            status = st[-1]
            check_name = st[0]
            if status == 'PASS':
                p += 1
                all_result_table.append([check_name, TBL_CELL_CONTENT_PASS, 'N/A', 'N/A'])
            elif status == 'FAIL':
                f += 1
                all_result_table.append([check_name, 'N/A', TBL_CELL_CONTENT_FAIL, 'N/A'])
            elif status == 'ERROR':
                e += 1
                all_result_table.append([check_name, 'N/A', 'N/A', TBL_CELL_CONTENT_ERROR])

            else:
                p = f = e = -1
        summary_table.append([sd.get('runbook'), str(str(p) + ' / ' + str(f) + ' / ' + str(e) + ' ( ' + str(p+f+e) + ' ) ')])

    s = '\x1B[1;20;46m' + "~~ Summary ~~" + '\x1B[0m'
    print(s)

    print(tabulate(all_result_table, headers='firstrow', tablefmt='fancy_grid'))
    print("")
    print(tabulate(summary_table, headers='firstrow', tablefmt='fancy_grid'))


def update_current_execution(status, id: str, content: dict):
    """update_failed_execution This function gets execution id that has failed and will
       create a dynamic failed runbook. And update the execution_summary.yaml file
       to record the last failed run status

       :type status: CheckOutputStatus 
       :param status: Enum of type CheckOutputStatus that has the current status

       :type id: string 
       :param id: The Execution ID (Action UUID that failed)

       :type content: dict
       :param content: The NotebookNode dictionary that has all the cell contents

       :rtype: None
    """
    if content == {}:
        print("ERROR: Cannot Update Failed execution with No Content")
        return

    execution_file = os.environ.get('EXECUTION_DIR').strip('"') + '/execution_summary.yaml'
    failed_runbook = os.environ.get('EXECUTION_DIR').strip('"') + '/workspace/' + f"{id}.ipynb"

    
    # If failed directory does not exists, lets create it
    if os.path.exists(os.environ.get('EXECUTION_DIR').strip('"') + '/workspace') == False:
        os.mkdir(os.makedirs(os.environ.get('EXECUTION_DIR').strip('"') + '/workspace'))
    
    prev_status = None
    es = {}
    try:
        es = get_pss_record('current_execution_status')
    except:
        pass 
    finally:
        if es != {}:
            if id in es.get('exec_status').keys():
                prev_status = es['exec_status'].get(id).get('current_status')
            else:
                es['exec_status'][id] = {}
        else:
            es['exec_status'] = {}
            es['exec_status'][id] = {}
    
    es['exec_status'][id]['failed_runbook'] = failed_runbook
    es['exec_status'][id]['check_name'] = str(get_action_name_from_id(id, content))
    es['exec_status'][id]['current_status'] = status
    es['exec_status'][id]['connector_type'] = str(get_connector_name_from_id(id, content))
    
    if status == prev_status:
        pass 
    
    if CheckOutputStatus(status) == CheckOutputStatus.SUCCESS:
        es['exec_status'][id]['passed_timestamp'] = str(datetime.now())
    else:
        es['exec_status'][id]['failed_timestamp'] = str(datetime.now())
    
    upsert_pss_record('current_execution_status', es)


    # Lets create the failed ipynb
    try:
        nb = nbformat.v4.new_notebook()
        for c in content.get('cells'):
            if c.get('metadata').get('action_uuid') == id:
                nb['cells'].append(c)
    except Exception as e:
        pass
    finally:
        nbformat.write(nb, failed_runbook)
    
    if os.path.exists(failed_runbook) != True:
        print(f"ERROR Unable to create failed runbook at {failed_runbook}")

def create_jit_runbook(check_list: list):
    """create_jit_runbook This function creates Just In Time runbook
       with just one code cell. The content will be upended with the
       task lines... and used it create the jit runbook

       :type check_list: list
       :param check_list: List of checks in the form of dictionary 

       :type id: str 
       :param id: Action UUID 

       :rtype: None
    """
    nb = nbformat.v4.new_notebook()
    failed_notebook = os.environ.get('EXECUTION_DIR').strip('"') + '/workspace/' + str(uuid.uuid4()) + '.ipynb'
    for check in check_list:
        s_connector = check.get('metadata').get('action_type')
        s_connector = s_connector.replace('LEGO', 'CONNECTOR')
        cred_name,cred_id = get_creds_by_connector(s_connector)
        task_lines = '''
task.configure(printOutput=True)
task.configure(credentialsJson=\'\'\'{
        \"credential_name\":''' +  f" \"{cred_name}\"" + ''',
        \"credential_type\":''' + f" \"{s_connector}\"" + ''',
        \"credential_id\":''' +  f" \"{cred_id}\"" + '''}\'\'\')
        '''
    
        try:
            c = check.get('code')
            idx = c.index("task = Task(Workflow())")
            c = c[:idx+1] + task_lines.split('\n') + c[idx+1:]
            check['code'] = []
            for line in c[:]:
                check['code'].append(str(line + "\n"))
            
            check['metadata']['action_uuid'] = check['uuid']
            check['metadata']['name'] = check['name']
            cc = nbformat.v4.new_code_cell(check.get('code'))
            for k,v in check.items():
                if k != 'code':
                    cc[k] = check[k]
            nb['cells'].append(cc)

        except Exception as e:
            raise e
            
    nbformat.write(nb, failed_notebook)
    return failed_notebook
    

def update_check_run_trail(id: str, action_name: str, connector_type: str, result: CheckOutputStatus, data : dict = {}):
    """update_check_run_trail This function updates PSS for checks_run_trail entry
       
       :type id: str
       :param id: Action UUID to update entry in the audit log

       :type action_name: str
       :param action_name: Action Name

       :type connector_type: str
       :param connector_type: Connector Type like AWS, GCP, etc...

       :type result: CheckOutputStatus
       :param result: Output Status as an Enum of type CheckOutputStatus

       :type data: dict (Optional Variable)
       :param data: Data in the form of a python Dictionary.

       :rtype: None
    """
    content = {}
    try:
        content = get_pss_record('check_run_trail')
    except:
        pass
    finally:
        k = str(datetime.now())
        temp_trail = {}
        temp_trail[id] = {} 
        temp_trail[id]['time_stamp'] = k
        temp_trail[id]['action_uuid'] = id 
        temp_trail[id]['check_name'] = action_name
        temp_trail[id]['connector_type'] = connector_type.upper()
        s = ''
        if result == CheckOutputStatus.SUCCESS:
            s = "PASS"
        elif result == CheckOutputStatus.FAILED:
            s = "FAILED"
        elif result == CheckOutputStatus.RUN_EXCEPTION:
            s = "ERRORED"
        temp_trail[id]['status'] = s 
        if data != {}:
            temp_trail[id]['failed_objects'] = data
            print("UPdATING FAILED OBJECT")
        content.update(temp_trail)

    upsert_pss_record('check_run_trail', content)

def update_audit_trail(status_dict_list: list):
    """update_audit_trail This function will update the satus of each run of the runbook

       :type status_dict_list: list
       :param status_dict: List of Python Dictionary that has the status for all the checks that 
             were run for the given runbook run

       :rtype: None
    """
    content = {}
    trail_data = {}
    try:
        content = get_pss_record('audit_trail')
    except:
        pass
    finally:
        k = str(datetime.now())
        p = f = e = 0
        id = uuid.uuid4()
        trail_data = {}
        trail_data[id] = {} 
        trail_data[id]['time_stamp'] = k
        trail_data[id]['check_status'] = {}
        for sd in status_dict_list:
            if sd == {}:
                continue 
            for s in sd.get('result'):
                check_name,check_id,connector,status = s
                if status == 'PASS':
                    p += 1
                elif status == 'FAIL':
                    f += 1
                elif status == 'ERROR':
                    e += 1
                trail_data[id]['check_status'][check_id] = {}
                trail_data[id]['check_status'][check_id]['check_name']= check_name 
                trail_data[id]['check_status'][check_id]['status'] = status
                trail_data[id]['check_status'][check_id]['connector'] = connector
                
        trail_data[id]['summary'] = f"Summary (total/p/f/e): {p+e+f}/{p}/{f}/{e}"
    upsert_pss_record('audit_trail', trail_data)

def list_checks_by_connector(connector_name: str):
    """list_checks_by_connector This function reads the ZoDB and displays the
       checks by a given connector. connector_name can be `all` in that case
       all the checks across connectors performed and displayed.

       :type connector_name: string
       :param connector_name: Connector name like aws, gcp, etc... or all for everything

       :rtype: None
    """
    list_connector_table = [[TBL_HDR_LIST_CHKS_CONNECTOR, TBL_HDR_CHKS_NAME, TBL_HDR_CHKS_UUID]]
    for l in get_checks_by_connector(connector_name):
        list_connector_table.append(l)
   
    print("")
    print(tabulate(list_connector_table, headers='firstrow', tablefmt='fancy_grid'))
    print("")


def display_failed_checks(connector: str = ''):
    """display_failed_checks This function reads the execution_summary.yaml and displays
       the last failed checks with its UUID and Action.

       :rtype: None
    """
    pss_content = get_pss_record('current_execution_status')
    exec_status = pss_content.get('exec_status')
    failed_exec_list = []
    if exec_status != None:
        for k,v in exec_status.items():
            if CheckOutputStatus(v.get('current_status')) == CheckOutputStatus.FAILED:
                d = {}
                d['check_name'] = v.get('check_name')
                d['timestamp'] = v.get('failed_timestamp')
                d['execution_id'] = k 
                if connector == 'all':
                    failed_exec_list.append(d)
                elif connector not in ('', None) and v.get('connector_type') == connector.lower():
                    # Append only when connector type matches
                    failed_exec_list.append(d)
                else:
                    print(f"NO RESULTS FOUND TYPE: {connector}")
                    return

    failed_checks_table = [[TBL_HDR_DSPL_CHKS_NAME, TBL_HDR_DSPL_CHKS_UUID]]
    for failed in failed_exec_list:
        failed_checks_table.append([failed.get('check_name') + '\n' + '( Last Failed On: ' + failed.get('timestamp') +' )', 
                                    failed.get('execution_id')])
    
    print("")
    print(tabulate(failed_checks_table, headers='firstrow', tablefmt='fancy_grid'))
    print("")



def show_audit_trail(filter: str = None):
    """display_failed_logs This function reads the failed logs for a given execution ID
       When a check fails, the failed logs are saved in os.environ['EXECUTION_DIR']/failed/<UUID>.log

    :type filter: string
    :param filter: filter used to query audit_trail to get logs used to serach logs
    """
    if filter == None:
        filter = 'all'
    
    pss_content = get_pss_record('audit_trail')

    s = '\x1B[1;20;42m' + "~~~~ CLI Used ~~~~" + '\x1B[0m'
    print("")
    print(s)
    print("")
    print(f"\033[1m {sys.argv[0:]} \033[0m")
    print("")

    if filter.lower() == 'all':
        all_result_table = [["\033[1m Execution ID \033[0m", 
                             "\033[1m Execution Summary \033[0m", 
                             "\033[1m Execution Timestamp \033[0m"]]
        for item in pss_content.items():
            k,v = item
            summary_text = "\033[1m" + v.get('summary') + "\033[0m"
            each_row = [[k, summary_text, v.get('time_stamp')]]
            all_result_table += each_row

        print(tabulate(all_result_table, headers='firstrow', tablefmt='fancy_grid'))
        return

    exec_content = {}
    try:
        exec_content = get_pss_record('check_run_trail')
    except:
        pass
    finally:
        if exec_content == {}:
            print("SYSTEM ERROR: Not able to print trail logs")
            return 
    connector_result_table = [["\033[1m Execution ID \033[0m", 
                             "\033[1m Check ID \033[0m \n \033[1m (Check Name) \033[0m", 
                             "\033[1m Run Status \033[0m",
                             "\033[1m Time Stamp \033[0m"]]
    single_result_table = [["\033[1m Execution ID \033[0m", 
                             "\033[1m Failed Objects \033[0m", 
                             "\033[1m Run Status \033[0m",
                             "\033[1m Time Stamp \033[0m"]]
    flag = -1
    for item in pss_content.items():
        k,v = item
        for l,m in v.items():
            if l == 'check_status':
                for k1,v1 in m.items():
                    print(f"{v}")
                    if filter.lower() == k1:
                        flag = 1
                        single_result_table += [[k, 
                                      v1.get('failed_objects'),
                                      v1.get('status'), 
                                      v.get('time_stamp')]]
                        break
                    elif filter.lower() == v1.get('connector'):
                        flag = 2
                        connector_result_table += [[k, k1 + '\n' + '( ' + v1.get('check_name') + ' )', v1.get('status'), v.get('time_stamp')]]
                        #pprint.pprint(f"{k} {k1} {v1}")
            
    if flag == 1:
        print(tabulate(single_result_table, headers='firstrow', tablefmt='fancy_grid'))
    elif flag == 2:
        print(tabulate(connector_result_table, headers='firstrow', tablefmt='fancy_grid'))

def read_ipynb(filename: str) -> nbformat.NotebookNode:
    """read_ipynb This function takes the Runbook name and reads the content
           using nbformat.read, Reads as Version 4.0 and returns the 
           notebooknode.

       :type filename: str 
       :param filename: Runbook name

       :rtype: NotebookNode 
    """
    nb = None
    if os.path.exists(filename) != True:
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
            if cell.get('metadata').get('tags') != None:
                tags = None
                if (isinstance(cell.get('metadata').get('tags'), list)) == True:
                    if len(cell.get('metadata').get('tags')) != 0:
                        tags = cell.get('metadata').get('tags')[0]
                else:
                    tags = None

                if "unSkript:nbParam" != tags:
                    if cell.get('metadata').get('action_uuid') != None:
                        retval.append(cell.get('metadata').get('action_uuid'))
            else:
                if cell.get('metadata').get('action_uuid') != None:
                    retval.append(cell.get('metadata').get('action_uuid'))
    
    return retval 

def get_last_code_cell_output(content: dict) -> dict:
    """get_last_code_cell_output This function takes in the notenode dictionary
           finds out the last cell output and returns in the form of a dict

       :type content: dict 
       :param content: Notenode as Dictionary

       :rtype: Last output in the form of Python dictionary  
    """
    retval = {}
    if content in ('', None):
        print("Content sent is empty")
        return retval

    for cell in content.get('cells'):
        if cell.get('cell_type') == 'code':
            if cell.get('id') == 'lastcell':
                outputs = {}
                outputs = cell.get('outputs')
                retval = outputs
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
            retval = cell.get('metadata').get('action_type').replace('LEGO_TYPE_', '').lower()
    
    return retval

def create_creds_mapping():
    """create_creds_mapping This function creates a credential ZoDB collection with the name
       default_credential_id. The mapping will be based on the Credential TYPE, he mapping would
       be a list of dictionaries with {"name", "id"}

       This function reads the credentials directory for all the available credentials and updates
       the ZoDB with the mapping. 

       :rtype: None
    """
    creds_files = os.environ.get('HOME').strip('"') + CREDENTIAL_DIR + '/*.json'
    list_of_creds = glob.glob(creds_files)
    d = {}
    for creds in list_of_creds:
        with open(creds, 'r') as f:
            c_data = json.load(f)
            d[c_data.get('metadata').get('type')] = {"name": c_data.get('metadata').get('name'), "id": c_data.get('metadata').get('id')}
    upsert_pss_record('default_credential_id', d, False)

if __name__ == "__main__":
    try:
        if os.environ.get('EXECUTION_DIR') == None:
            os.environ['EXECUTION_DIR'] = "/data/execution"
        # If failed directory does not exists, lets create it
        if os.path.exists(os.environ.get('EXECUTION_DIR').strip('"') + '/workspace') == False:
            os.mkdir(os.makedirs(os.environ.get('EXECUTION_DIR').strip('"') + '/workspace'))
        
        create_creds_mapping()
        load_or_create_global_configuration()
    except Exception as e:
        raise e 
    
    parser = argparse.ArgumentParser(prog='unskript-client')
    version_number = "0.1.0"
    description=""
    description = description + str("\n")
    description = description + str("\t  Welcome to unSkript CLI Interface \n")
    description = description + str(f"\t\t   VERSION: {version_number} \n")
    parser.description = description
    parser.add_argument('-lr', '--list-runbooks', help='List Available Runbooks', action='store_true')
    parser.add_argument('-rr', '--run-runbook', type=str, help='Run the given runbook')
    parser.add_argument('-rc', '--run-checks', type=str, help='Run all available checks [all | connector | failed]')
    parser.add_argument('-df', '--display-failed-checks', help='Display Failed Checks [all | connector]')
    parser.add_argument('-lc', '--list-checks', type=str, help='List available checks, per connector or all')
    parser.add_argument('-sa', '--show-audit-trail', type=str, help='Show audit trail [all | connector | execution_id]')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    if args.list_runbooks == True: 
        list_runbooks()
    elif args.run_runbook not in  ('', None):
        run_ipynb(args.run_runbook)
    elif args.run_checks not in ('', None):
        run_checks(args.run_checks)
    elif args.display_failed_checks not in ('', None):
        display_failed_checks(args.display_failed_checks)
    elif args.list_checks not in ('', None):
        list_checks_by_connector(args.list_checks)
    elif args.show_audit_trail not in ('', None):
        show_audit_trail(args.show_audit_trail)
    else:
        parser.print_help() 
