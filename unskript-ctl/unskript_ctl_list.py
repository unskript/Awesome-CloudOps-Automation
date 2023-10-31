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

from tabulate import tabulate
from argparse import ArgumentParser, REMAINDER, SUPPRESS


# LIST OF CONSTANTS USED IN THIS FILE
TBL_HDR_RUNBOOK_FILENAME="\033[1m Runbook File \033[0m"


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
    table = [["File Name",  "Runbook Name"]]
    for runbook in runbooks:
        contents = None
        with open(runbook, 'r') as f:
            contents = f.read()
        try:
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

def list_main():
    parser = ArgumentParser(description='-l | --list options')
    parser.add_argument('-l',
                        '--list',
                        help=SUPPRESS,
                        required=True,
                        action="store_false")
    parser.add_argument('--runbooks',
                        dest='runbooks',
                        help='List all runbooks present in the system',
                        action="store_false")
    
    args = parser.parse_args()

    if len(sys.argv) == 2:
        parser.print_help()
        sys.exit(0)

    pass


if __name__ == '__main__':
    list_main()