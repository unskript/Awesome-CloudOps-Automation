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
import glob
import json
import sys
import os
import pprint 

from tabulate import tabulate
from argparse import ArgumentParser, REMAINDER, SUPPRESS
from unskript_utils import *
from db_utils import * 

# LIST OF CONSTANTS USED IN THIS FILE
TBL_HDR_RUNBOOK_FILENAME=f"{bcolors.BOLD} Runbook File {bcolors.ENDC}"
TBL_HDR_RUNBOOK_NAME=f"{bcolors.BOLD} Runbook Name {bcolors.ENDC}"

# TO REMOVE
TBL_HDR_CHKS_NAME="\033[36m Checks Name \033[0m"
TBL_HDR_DSPL_CHKS_NAME="\033[35m Check Name \n (Last Failed) \033[0m"
TBL_HDR_DSPL_EXEC_ID="\033[1m Failed Execution ID \033[0m"
TBL_HDR_FAILED_OBJECTS="\033[1m Failed Objects \033[0m"
TBL_HDR_CHKS_FN="\033[1m Function Name \033[0m"
TBL_HDR_LIST_CHKS_CONNECTOR="\033[36m Connector Name \033[0m"


def display_failed_checks():
    """display_failed_checks This function reads the execution_summary.yaml and displays
       the last failed checks with its UUID and Action.
    """
    parser = ArgumentParser()
    parser.add_argument('-l',
                        '--list',
                        action="store_true",
                        help="List Option")
    parser.add_argument('--failed-checks',
                        help="Failed Checks",
                        action="store_true")
    parser.add_argument('--all',
                        help='Run all failed checks again',
                        action="store_true")
    parser.add_argument('--type',
                        dest='connector_type',
                        choices=CONNECTOR_LIST,
                        help="Connector Type to display the failed check against",
                        type=str)
    args = parser.parse_args(sys.argv[1:])

    if len(sys.argv) == 2:
        parser.print_help()
        sys.exit(0)

    connector = ""
    if args.all is True:
        connector = 'all'
    elif args.connector_type not in ('', None):
        connector = args.connector_type
    else:
        parser.print_help()
        sys.exit(0)
    
    s = '\x1B[1;20;42m' + "~~~~ CLI Used ~~~~" + '\x1B[0m'
    print("")
    print(s)
    print("")
    print(f"\033[1m {sys.argv[0:]} \033[0m")
    print("")

    

    pss_content = {}
    try: 
        pss_content = get_pss_record('audit_trail')
    except:
        pass 

    failed_checks_table = [[TBL_HDR_DSPL_CHKS_NAME, TBL_HDR_FAILED_OBJECTS, TBL_HDR_DSPL_EXEC_ID]]
    
    for exec_id in pss_content.keys():
        execution_id = exec_id 
        for check_id in pss_content.get(exec_id).get('check_status').keys():
            if pss_content.get(exec_id).get('check_status').get(check_id).get('status').lower() == "fail":
                if connector == 'all':
                    failed_checks_table += [[
                        pss_content.get(exec_id).get('check_status').get(check_id).get('check_name') + '\n' + f"(Test Failed on: {pss_content.get(exec_id).get('time_stamp')})",
                        pprint.pformat(pss_content.get(exec_id).get('check_status').get(check_id).get('failed_objects'), width=10),
                        execution_id
                    ]]
                elif connector.lower() == pss_content.get(exec_id).get('check_status').get(check_id).get('connector').lower():
                    failed_checks_table += [[
                        pss_content.get(exec_id).get('check_status').get(check_id).get('check_name') + '\n' + f"(Test Failed on: {pss_content.get(exec_id).get('time_stamp')})",
                        pprint.pformat(pss_content.get(exec_id).get('check_status').get(check_id).get('failed_objects'), width=10),
                        execution_id
                    ]]

    print("")
    print(tabulate(failed_checks_table, headers='firstrow', tablefmt='fancy_grid'))
    print("")


def list_runbooks():
    """list_runbooks This is simple routine that uses python glob to fetch
    the list of runbooks stored in the $HOME directory. 
    """
    home_directory = os.environ.get('HOME')
    
    runbooks = []
    for root, dirs, files in os.walk(home_directory):
        for _file in files:
            if _file.endswith(".ipynb"):
                runbooks.append(os.path.join(root, _file))

    runbooks.sort()
    table = [[TBL_HDR_RUNBOOK_FILENAME,  TBL_HDR_RUNBOOK_NAME]]
    for runbook in runbooks:
        contents = None

        try:
            with open(runbook, 'r') as f:
                contents = f.read()
            if contents:
                contents = json.loads(contents)
                if contents.get('metadata') \
                   and contents.get('metadata').get('execution_data') \
                   and contents.get('metadata').get('execution_data').get('runbook_name'):
                    name = contents.get('metadata').get(
                         'execution_data').get('runbook_name')
                    filename = os.path.basename(runbook)
                    table.append([filename, name])
        except Exception as e:
            print(e)
            pass

    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

def list_credentials():
    """list_credentials Lists the credentials and their status (ACTIVE or INACTIVE) same as how
       we display on the UI. ACTIVE means the credential data has been filled and ready to go
       INACTIVE means the credential is not yet ready to be used.
    """ 
    active_creds = []
    incomplete_creds = []

    creds_files = os.environ.get('HOME').strip('"') + CREDENTIAL_DIR + '/*.json'
    list_of_creds = glob.glob(creds_files)

    for creds in list_of_creds:
        with open(creds, 'r') as f:
            c_data = json.load(f)

            connector_type = c_data.get('metadata').get('type')
            connector_name = c_data.get('metadata').get('name')

            if c_data.get('metadata') and c_data.get('metadata').get('connectorData') != "{}":
                active_creds.append((connector_type, connector_name))
            else:
                incomplete_creds.append((connector_type, connector_name))

    combined_list = active_creds + incomplete_creds

    headers = ["#", "Connector Type", "Connector Name", "Status"]
    table_data = [headers]

    for index, (ctype, cname) in enumerate(combined_list, start=1):
        status = "Active" if index <= len(active_creds) else "Incomplete"
        table_data.append([index, ctype, cname, status])

    print(tabulate(table_data, headers='firstrow', tablefmt='fancy_grid'))

def list_checks_by_connector():
    """list_checks_by_connector This function reads the ZoDB and displays the
       checks by a given connector. connector_name can be `all` in that case
       all the checks across connectors performed and displayed.

       :rtype: None
    """
    parser = ArgumentParser(description='-c | --checks')
    parser.add_argument('-l',
                        '--list',
                        action="store_true",
                        help="List Option")
    parser.add_argument('-c',
                        '--checks',
                        action='store_true',
                        help="List Checks")
    parser.add_argument('-a',
                        '--all',
                        help="List all Checks across connectors in the system",
                        action="store_true")
    parser.add_argument('-t',
                        '--type',
                        choices=CONNECTOR_LIST,
                        help="Type of connector for which the checks should be shown")

    args = parser.parse_args()

    if len(sys.argv) <= 2:
        parser.print_help()
        sys.exit(0)


    if args.all is True:
        connector_name = 'all'
    elif args.type not in ('', None):
        connector_name = args.type
    else:
        connector_name = 'all'

    list_connector_table = [
        [TBL_HDR_LIST_CHKS_CONNECTOR, TBL_HDR_CHKS_NAME, TBL_HDR_CHKS_FN]]
    for l in get_checks_by_connector(connector_name):
        list_connector_table.append(l)

    print("")
    print(tabulate(list_connector_table, headers='firstrow', tablefmt='fancy_grid'))
    print("")

def list_main():
    lp = ArgumentParser()
    lp.add_argument('-l',
                    '--list',
                    action='store_true',
                    help=SUPPRESS)
    lp.add_argument('-r',
                    '--runbooks',
                    action='store_true',
                    help='List Runbooks')
    lp.add_argument('--failed-checks',
                    type=str,
                    nargs=REMAINDER,
                    help='List Failed checks')
    lp.add_argument('-c',
                    '--checks',
                    nargs=REMAINDER,
                    help='List Checks')
    lp.add_argument('--credential',
                    action="store_true",
                    help="List Credential")
    largs = lp.parse_args(sys.argv[1:])
    
    
    if len(sys.argv) <= 2:
        lp.print_help()
        sys.exit(1)

    if largs.runbooks:
        list_runbooks()
    elif largs.checks:
        list_checks_by_connector()
    elif largs.credential:
        list_credentials()
    elif largs.failed_checks not in ('', None):
        display_failed_checks()
    else:
        lp.print_help()
        sys.exit(1)
    

if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument("-l",
                         "--list",
                        nargs=REMAINDER,
                        help="List items")
    args = parser.parse_args()

    if len(sys.argv) <= 2: 
        parser.print_help()
        sys.exit(1)
    
    if args.list:
        list_main()
