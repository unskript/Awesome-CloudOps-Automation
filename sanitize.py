#!/usr/bin/env python
#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import os
import json
import re
import ast
import sys

try:
    from git import Repo
except:
    print("THIS SCRIPT NEEDS PIP PACKAGE NAMED `gitpython` Please install it before running this script.")
    raise Exception("Python package gitpython is needed to run this script.")

def sanitize(ipynbFile: str = '') -> bool:
    retVal = False
    if not ipynbFile:
        print("ERROR: IPYNB file is needed")
        return retVal

    with open(ipynbFile) as f:
        nb = json.loads(f.read())

        execution_data = {
            'runbook_name': nb.get('metadata').get('execution_data').get('runbook_name'),
            'parameters': nb.get('metadata').get('execution_data').get('parameters'),
        }

    new_cells = []
    cells = nb.get("cells")
    for cell in cells:
        # Lets make sure Cell Metadata has tags, only then check if it matches the first cell
        if cell.get('metadata').get('tags') and 'unSkript:nbParam' in cell.get('metadata').get('tags'):
            print("SKIPPING FIRST CELL")
            continue

        cell_type = cell.get('cell_type')
        if cell_type == 'code':
            # Reset CredntialsJson
            cell['metadata']['credentialsJson'] = {}

            # Cleanout output
            cell['outputs'] = []

            # Delete source CredntialsJson
            skip_pattern = "task.configure(credentialsJson="
            cell_source = []
            skip = False
            for line in cell.get('source'):
                if skip_pattern in line:
                    skip = True
                elif skip and line.strip() == "}''')":
                    skip = False
                elif not skip:
                    cell_source.append(line)

            cell['source'] = cell_source

        new_cells.append(cell)

    nb_new = nb.copy()
    nb_new["cells"] = new_cells
    try:
        # Reset Environment & Tenant Information
        nb_new['metadata']['execution_data'] = execution_data

    except:
        pass

    with open(ipynbFile, 'w') as f:
        json.dump(nb_new, f, indent=1)
        retVal = True

    return retVal


if __name__ == '__main__':
    # Find out All changed files in the PR
    try:
        repo = Repo('.', search_parent_directories=True)
    except Exception as e:
        raise e

    if len(sys.argv) > 1:
        filelist = sys.argv[1:]
    else:
        filelist = [item.a_path for item in repo.index.diff(None)]

    if not filelist:
        print("No update needed")
        sys.exit(0)

    for f in filelist:
        # To handle file delete case, check if the file exists.
        if os.path.isfile(f) is False:
            continue
        print(f"Processing {f}")
        if f.endswith('.ipynb'):
            if sanitize(f):
                print(u'\u2713', f"Updated Notebook {f}")
        else:
            print(f"Skipping {f} as it is not a ipynb file")

    sys.exit(0)
