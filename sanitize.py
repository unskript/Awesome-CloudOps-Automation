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

    new_cells = []
    cells = nb.get("cells")
    for cell in cells:
        # Lets make sure Cell Metadata has tags, only then check if it matches the first cell
        if cell.get('metadata').get('tags') and 'unSkript.nbParam' in cell.get('metadata').get('tags'):
            print("SKIPPING FIRST CELL")
            continue

        cell_type = cell.get('cell_type')
        if cell_type == 'code':
            # Reset CredntialsJson
            cell['metadata']['credentialsJson'] = {}
            # Cleanout output
            cell['output'] = {}
            # Delete source CredntialsJson
            del_cred = re.sub(r"(task.configure\(credentialsJson.*?\'\'\'\))","", str(cell['source']), re.DOTALL)
            cell['source'] = ast.literal_eval(del_cred)
        new_cells.append(cell)

    nb_new = nb.copy()
    nb_new["cells"] = new_cells
    try:
        # Reset Environment & Tenant Information
        nb_new['metadata']['execution_data']['environment_id'] = ''
        nb_new['metadata']['execution_data']['environment_name'] = ''
        nb_new['metadata']['execution_data']['tenant_id'] = ''
        nb_new['metadata']['execution_data']['tenant_url'] = ''
        nb_new['metadata']['execution_data']['user_email_id'] = ''
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
        if f.endswith('.ipynb'):
            if sanitize(f):
                print(u'\u2713', f"Updated Notebook {f}")
        else:
            print(f"Skipping {f} as it is not a ipynb file")

    sys.exit(0)
