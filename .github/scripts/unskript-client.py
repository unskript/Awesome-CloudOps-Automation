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

from tabulate import tabulate
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
from unskript.legos.utils import CheckOutput, CheckOutputStatus

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
TBL_HDR_CHKS_NAME="\033[36m Checks Name \033[0m"
TBL_HDR_CHKS_PASS="\033[32m Passed Checks \033[0m"
TBL_HDR_CHKS_FAIL="\033[35m Failed Checks \033[0m"
TBL_HDR_CHKS_ERROR="\033[31m Errored Checks \033[0m"
TBL_HDR_RBOOK_NAME="\033[36m Runbook Name \033[0m"
TBL_HDR_CHKS_COUNT="\033[32m Checks Count (Pass/Fail/Error) (Total checks) \033[0m"
TBL_CELL_CONTENT_PASS="\033[1m PASS \033[0m"
TBL_CELL_CONTENT_FAIL="\033[1m FAIL \033[0m"
TBL_CELL_CONTENT_ERROR="\033[1m ERROR \033[0m"



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
    else:
        # CREATE FILE WITH SOME PLACEHOLDER KEYS
        temp_content = {}
        temp_content['runbook_dir'] = os.environ.get('HOME') + "/runbooks"
        temp_content['execution_dir'] = '/data/execution'
        temp_content['display_execution_output'] = True
        temp_content['envs'] = {"SOME_KEY": "SOME_VALUE"}
        with open(GLOBAL_CONFIG_PATH, 'w') as f:
            yaml.safe_dump(temp_content, f)
        
        global_content = temp_content
    
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

def run_all(filter: str):
    """run_all This function takes the filter as an argument
       if the filter is all, then all Runbooks in the $HOME/runbooks directory
       is selected to run. If a filter is given like aws, kubernetes, postgresql
       then all runbooks from that connector type will be run

       :type filter: str
       :param filter: Filter Name (Connector Name) Runbooks are stored in connectors

       :rtype: None
    """
    runbooks = []
    runbook_dir = os.environ.get('RUNBOOK_DIR')
    runbook_dir = runbook_dir.strip('"')
    if runbook_dir == None:
        print("SYSTEM ERROR")
        return 
    
    if filter == 'all':
        f = runbook_dir.strip() + '/' + '*/*.ipynb'
    else:
        f = runbook_dir.strip() + '/' + filter.lower().strip() + '/*.ipynb'

    runbooks = glob.glob(f)
    runbooks.sort()
    
    status_list_of_dict = []

    for r in runbooks:
        run_ipynb(r, status_list_of_dict)

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

    pass


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
        outputs = get_last_code_cell_output(nb.dict())
    
    ids = get_code_cell_action_uuids(nb.dict())
    result_table = [["Checks Name", "Result", "Failed Count", "Error"]]
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
                status_dict['result'].append([get_action_name_from_id(ids[idx], nb.dict()), 'PASS'])
            elif CheckOutputStatus(payload.get('status')) == CheckOutputStatus.FAILED: 
                failed_objects = payload.get('objects')
                failed_result[get_action_name_from_id(ids[idx], nb.dict())] = failed_objects 
                result_table.append([get_action_name_from_id(ids[idx], nb.dict()), TBL_CELL_CONTENT_FAIL, len(failed_objects), 'N/A'])
                failed_result_available = True
                status_dict['result'].append([get_action_name_from_id(ids[idx], nb.dict()), 'FAIL'])
            elif CheckOutputStatus(payload.get('status')) == CheckOutputStatus.RUN_EXCEPTION:
                result_table.append([get_action_name_from_id(ids[idx], nb.dict()), TBL_CELL_CONTENT_ERROR, 0, payload.get('error')])
                status_dict['result'].append([get_action_name_from_id(ids[idx], nb.dict()), 'ERROR'])
        except Exception as e:
            pass
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

def usage() -> str:
    """usage  This is a help function that lists the options availble
            to use this function. This gets triggered if insufficient parameters
            or insufficient parameters are sent.
    """
    retval = ''
    version_number = '0.0.1'
    retval = retval + str("\n")
    retval = retval + str("\t  Welcome to unSkript CLI Interface \n")
    retval = retval + str(f"\t\t   VERSION: {version_number} \n")
    retval = retval + str("\n")
    retval = retval + str("\t  Usage: \n")
    retval = retval + str("\t     unskript-client.py <COMMAND> <ARGS> \n")
    retval = retval + str("\n")
    retval = retval + str("\t     Examples -  \n")
    retval = retval + str("\t         unskript-client.py -lr / --list-runbooks \n")
    retval = retval + str("\t         unskript-client.py -rr / --run-runbook ~/runbooks/<RUNBOOK_NAME> \n")
    retval = retval + str("\t         unskript-client.py -ra / --run [all | connector] \n")
    retval = retval + str("")

    return retval

def list_runbooks():
    """list_runbooks  This is simple routine that uses python glob to fetch
            the list of runbooks stored in the a predefined path ~/runbooks
            and prints the available runbook and prints in a tabular form.
    
    """
    runbooks = glob.glob(os.environ.get('HOME') + '/runbooks/*.ipynb')
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


if __name__ == "__main__":
    try:
        load_or_create_global_configuration()
    except Exception as e:
        raise e 
    
    parser = argparse.ArgumentParser(prog='unskript-client', usage=usage())
    parser.add_argument('-lr', '--list-runbooks', help='List Available Runbooks', action='store_true')
    parser.add_argument('-rr', '--run-runbook', type=str, help='Run the given runbook')
    parser.add_argument('-ra', '--run', type=str, help='Run all available runbooks')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        print(usage())
        sys.exit(0)

    if args.list_runbooks == True: 
        list_runbooks()
    elif args.run_runbook not in  ('', None):
        run_ipynb(args.run_runbook)
    elif args.run not in ('', None):
        run_all(args.run)
    else:
        print(usage())
    