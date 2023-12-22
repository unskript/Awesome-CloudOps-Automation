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
import yaml
import json
import os
import pprint 
import sys

from tabulate import tabulate
from argparse import ArgumentParser, REMAINDER, SUPPRESS
from unskript_utils import *
from db_utils import * 

def display_failed_logs():
    parser = ArgumentParser()
    parser.add_argument('-s',
                        '--show',
                        action='store_true')
    parser.add_argument('--failed-logs',
                        action="store_true",
                        help="Display Failed Logs")
    parser.add_argument('--execution_id',
                        help="Execution ID for which the Logs should be fetched",
                        type=str)

    args = parser.parse_args()

    if len(sys.argv) <= 2:
        parser.print_help()
        sys.exit(0)

    if args.execution_id not in ('', None):
        exec_id = args.execution_id
    else:
        print(f"ERROR: Execution ID missing")
        parser.print_help()
        sys.exit(0)
    
    output = UNSKRIPT_EXECUTION_DIR + "/" + f"{exec_id}_output.txt"
    if os.path.exists(output) is False:
        print(
            f"\033[1m No Execution Log Found for Execution ID: {exec_id} \033[0m")
        return
    d_output = []
    with open(output, 'r') as f:
        d_output = json.loads(f.read())

    print("\033[1mFAILED OBJECTS \033[0m \n")
    for o in d_output:
        if o.get('status') != 1:
            print(f"\033[1m{o.get('name')} \033[0m")
            p = yaml.safe_dump(o.get('objects'))
            print(p)
            print("\n")


def show_audit_trail():
    """show_audit_trail This function reads the failed logs for a given execution ID
       When a check fails, the failed logs are saved in os.environ['EXECUTION_DIR']/failed/<UUID>.log
    :type filter: string
    :param filter: filter used to query audit_trail to get logs used to search logs
    """
    parser = ArgumentParser(description='-s | --show')
    parser.add_argument('-s',
                        '--show',
                        action='store_true')
    parser.add_argument('--audit-trail',
                        help="Audit Trail",
                        action='store_true')
    parser.add_argument('--all',
                        dest="all",
                        help="List Logs of All check across all connectors",
                        action="store_true")
    parser.add_argument('--type',
                        dest='connector_type',
                        help='Show Audit trail for checks for the given connector',
                        type=str)
    parser.add_argument('--execution_id',
                        type=str,
                        help='Execution ID for which the audit trail should be shown')

    args = parser.parse_args(sys.argv[1:])
    filter = 'all'

    pss_content = get_pss_record('audit_trail')

    if len(sys.argv) <= 3:
        parser.print_help()
        sys.exit(1)

    s = f"{bcolors.ARG_START}" + "~~~~ CLI Used ~~~~" + f"{bcolors.ARG_END}"
    print("")
    print(s)
    print("")
    print(f"{bcolors.BOLD} {sys.argv[0:]} {bcolors.ENDC}")
    print("")

    if args.all:
        print_all_result_table(pss_content=pss_content)
    elif args.connector_type not in ('', None):
        filter = args.connector_type
        print_connector_result_table(pss_content=pss_content, connector=filter)
    elif args.execution_id not in ('', None):
        filter = args.execution_id
        print_execution_result_table(pss_content=pss_content, execution_id=filter)



def print_all_result_table(pss_content: dict):
    if not pss_content:
        return 
    
    all_result_table = [["\033[1m Execution ID \033[0m",
                        "\033[1m Execution Summary \033[0m",
                        "\033[1m Execution Timestamp \033[0m"]]
    for item in pss_content.items():
        k, v = item
        summary_text = "\033[1m" + v.get('summary') + "\033[0m"
        check_names = "\033[1m" + str(k) + '\n' + "\033[0m"
        for k1, v1 in v.get('check_status').items():
            check_names += "    " + v1.get('check_name') + ' ['
            check_names += "\033[1m" + \
                v1.get('status') + "\033[0m" + ']' + '\n'
        each_row = [[check_names, summary_text, v.get('time_stamp')]]
        all_result_table += each_row

    print(tabulate(all_result_table, headers='firstrow', tablefmt='fancy_grid'))


def print_connector_result_table(pss_content: dict, connector: str):
    if not pss_content:
        return 
    
    connector_result_table = [["\033[1m Check Name \033[0m",
                            "\033[1m Run Status \033[0m",
                            "\033[1m Time Stamp \033[0m",
                            "\033[1m Execution ID \033[0m"]]
    
    for exec_id in pss_content.keys():
        execution_id = exec_id
        if pss_content.get(exec_id).get('check_status'):
            for check_id in pss_content.get(exec_id).get('check_status').keys():
                if pss_content.get(exec_id).get('check_status').get(check_id).get('connector').lower() == connector.lower():
                    connector_result_table += [[pss_content.get(exec_id).get('check_status').get(check_id).get('check_name'),
                                               pss_content.get(exec_id).get('check_status').get(check_id).get('status'),
                                               pss_content.get(exec_id).get('time_stamp'),
                                               execution_id]]

    print(tabulate(connector_result_table,
              headers='firstrow', tablefmt='fancy_grid'))
    return 


def print_execution_result_table(pss_content: dict, execution_id: str):
    execution_result_table = [["\033[1m Check Name \033[0m",
                            "\033[1m Failed Objects \033[0m",
                            "\033[1m Run Status \033[0m",
                            "\033[1m Time Stamp \033[0m"]]
    for exec_id in pss_content.keys():
        if exec_id == execution_id:
            ts = pss_content.get(exec_id).get('time_stamp')
            for check_ids in pss_content.get(exec_id).get('check_status').keys():
                execution_result_table += [[pss_content.get(exec_id).get('check_status').get(check_ids).get('check_name'),
                                            pprint.pformat(pss_content.get(exec_id).get('check_status').get(check_ids).get('failed_objects'), 30),
                                            pss_content.get(exec_id).get('check_status').get(check_ids).get('status'),
                                            ts]]

    print(tabulate(execution_result_table,
              headers='firstrow', tablefmt='fancy_grid'))



def show_main():
    sp = ArgumentParser()
    sp.add_argument("-s",
                    "--show",
                    help=SUPPRESS,
                    action="store_true")
    sp.add_argument("--audit-trail",
                    help="Show Audit Trail",
                    type=str,
                    nargs=REMAINDER)
    sp.add_argument("--failed-logs",
                    help="Show Failed Logs",
                    type=str,
                    nargs=REMAINDER)
    
    spargs = sp.parse_args(sys.argv[1:])

    if len(sys.argv) <= 2:
        sp.print_help()
        sys.exit(1)
    
    if spargs.audit_trail not in ('', None):
        show_audit_trail()
    elif spargs.failed_logs not in ('', None):
        display_failed_logs()

    pass 


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument("-s",
                         "--show",
                        dest="show_options",
                        nargs=REMAINDER,
                        help="Show Options")
    args = parser.parse_args()

    if len(sys.argv) <= 2:
        parser.print_help()
        sys.exit(1)
    
    if args.show_options:
        show_main()