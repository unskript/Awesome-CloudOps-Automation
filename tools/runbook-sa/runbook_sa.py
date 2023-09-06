"""This file runs static analysis using pyflakes on runbooks"""
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

import sys
import os
import time
import subprocess
import argparse

from nbformat import read
from datetime import datetime
from argparse import ArgumentParser, REMAINDER


def save_custom_cell_contents_to_file(runbook, output_file="./custom_cell_contents.py"):
    with open(runbook, 'r') as f:
        notebook_content = read(f, as_version=4)

    custom_cells = []
    globals_list = []
    globals_inserted = False
    for cell in notebook_content['cells'][1:]:
        if cell.get('cell_type') == "code":
            if cell.get('metadata').get('customAction') == True:
                # Get only custom cells putput
                custom_cells.append(cell)
            if cell.get('metadata').get('outputParams') != None:
                output_name = cell.get('metadata').get('outputParams').get('output_name')
                globals_list.append(output_name)
        else:
            # Cell is a Markdown cell
            pass
    
    if len(custom_cells) > 0:
        with open(output_file, 'w') as  f:
            for idx,cell in enumerate(custom_cells):
                if not cell.get('source'):
                    # If we have empty custom cell
                    continue 
                if not globals_inserted:
                    for g_list in globals_list:
                        f.write(f"{g_list} = None" + " # noqa" + '\n')
                    globals_inserted = True
                f.write(f"def custom_cell_{idx}(): \n")
                for line in cell.get('source').split('\n'):
                    f.write(f"    {line} \n")
                f.write('\n')
            f.write('\n')
        time.sleep(2)
        if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
            print(f"ERROR: Error occurred during extraction of custom cell for {runbook}")
    else:
        print("No Custom Cell Found in the Runbook")

def run_pyflakes(script):
    command = [f"pyflakes {script}"]
    process = subprocess.run(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
    if process.stdout == None:
        return process.stderr.decode('utf-8')
    else:
        return process.stdout.decode('utf-8')

def main(category: str = 'all', runbooks: list = []):
    if len(runbooks) == 0:
        print("Need an Input to run the script")
        sys.exit(-1)

    for idx,runbook in enumerate(runbooks):
        if not os.path.exists(runbook):
            print(f"Unable to find {runbook}...")
            continue
        print(f"Analyzing {runbook}")
        if category == 'custom':
            save_custom_cell_contents_to_file(runbook, f"./custom_cell_contents_{idx}.py")
            try:
                print(run_pyflakes(f'./custom_cell_contents_{idx}.py'))
            except Exception as e:
                raise e
        elif category == 'all':
            command = [f"jupyter nbconvert --to script {runbook}"]
            process = subprocess.run(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
            pyfile = runbook.replace('.ipynb', '.py')
            try:
                print(run_pyflakes(pyfile))
            except Exception as e:
                raise e
        

class CommaSeparatedAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(','))


if __name__ == '__main__':
    parser = ArgumentParser(prog='runbook-sa')
    version_number = "0.1.0"
    description = ""
    description = description + str("\n")
    description = description + str("\t  Welcome to Runbook Static Analysis Tool") + '\n'
    description = description + str(f"\t\t   VERSION: {version_number}") + '\n' 
    parser.description = description
    parser.epilog = 'This tool needs pyflakes and jupyter-lab to run'

    parser.add_argument('-ra', '--run-on-all-cells', 
                        dest='ra_runbooks',
                        action=CommaSeparatedAction,
                        help='Run Static Analysis on cells in the notebook -ra Runbook1,Runbook2, etc..')
    parser.add_argument('-rc', '--run-on-custom-cells', 
                        dest='rc_runbooks',
                        action=CommaSeparatedAction,
                        help='Run Static Analysis only on cells in the notebook -rc Runbook1,Runbook2, etc..')
    

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    if args.ra_runbooks:
        main(category='all', runbooks=args.ra_runbooks)
    elif args.rc_runbooks:
        main(category='custom', runbooks=args.rc_runbooks)
    else:
        parser.print_help()
        sys.exit(0)