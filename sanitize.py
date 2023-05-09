#!/usr/bin/env python
#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import os
import json
import sys
import argparse


## returns True is everything is ok 
def check_sanity(ipynbFile: str = '') -> bool:

    rc = True
    with open(ipynbFile) as f:
        nb = json.loads(f.read())

    jsonFile = ipynbFile.replace("ipynb", "json")
    with open(jsonFile) as jf:
        jsonData = json.loads(jf.read())

    if nb.get('metadata') == None:
        print("Failed metadata check for notebook")
        rc = False

    if nb.get('metadata').get('execution_data') == None:
        print("Failed execution_data check for notebook")
        rc = False

    exec_data = nb.get('metadata').get('execution_data')
    if len(exec_data) > 2:
        print("Failed execution_data keys check for notebook")
        rc = False

    if exec_data.get('runbook_name') == None:
        print("Failed runbook_name check for notebook")
        rc = False
    
    ## runbook_name should be same as the name in JSON file
    if exec_data.get('runbook_name') != jsonData.get('name'):
        print("Failed runbook_name value check for notebook")
        rc = False

    if exec_data.get('parameters') == None:
        print("Failed parameters value check for notebook")
        rc = False

    cells = nb.get("cells")
    for cell in cells:

        if cell.get('cell_type') == 'markdown':
            continue

        if cell.get('metadata') == None:
            print("Failed metadata check for cell")
            rc = False

        if cell.get('metadata').get('tags') == None:
            print("Failed metadata.tags check for cell")
            rc = False

        if 'unSkript:nbParam' in cell.get('metadata').get('tags'):
            print("Failed first cell check for cell")
            rc = False

        if cell.get('metadata').get('credentialsJson') != {}:
            print(f"Failed credentialJson/md check for cell, found {cell.get('metadata').get('credentialsJson')}")
            rc = False

        if cell.get('outputs') != []:
            print("Failed outputs check for cell")
            rc = False

        skip_pattern = "task.configure(credentialsJson="
        if skip_pattern in cell.get('source'):
            print("Failed credentialsJson/code check for cell")
            rc = False

    return rc


## returns True is everything is ok 
def sanitize(ipynbFile: str = '') -> bool:
    retVal = False
    if not ipynbFile:
        print("ERROR: IPYNB file is needed")
        return retVal

    jsonFile = ipynbFile.replace("ipynb", "json")
    with open(jsonFile) as jf:
        jsonData = json.loads(jf.read())

    with open(ipynbFile) as f:
        nb = json.loads(f.read())

        execution_data = {
            'runbook_name': jsonData.get('name'),
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
        print(u'\u2713', f"Updated Notebook {ipynbFile}")
        retVal = True

    return retVal


if __name__ == '__main__':

    # create argparse object
    parser = argparse.ArgumentParser(description='Process input files')

    # add argument for 'validate' mode
    parser.add_argument('-v', '--validate', action='store_true',
                        help='validate input files')

    # add argument for 'fix' mode
    parser.add_argument('-f', '--fix', action='store_true',
                        help='fix input files')

    # add positional argument for list of files
    parser.add_argument('files', nargs='+',
                        help='list of files to process')

    # parse arguments
    args = parser.parse_args()

    # default mode is validate
    validate_mode = True

    # check which mode is selected
    if args.validate:
        print('Running in validation mode')
        validate_mode = True
    elif args.fix:
        print('Running in fix mode')
        validate_mode = False

    # access the list of files
    filelist = args.files
    failedlist = []
    print('List of files:', filelist)

    for f in filelist:
        # To handle file delete case, check if the file exists.
        if os.path.isfile(f) is False:
            continue

        if f.endswith('.ipynb') is False:
            continue

        print(f"Processing {f}")
        if validate_mode is True:
            rc = check_sanity(f)
        else:
            rc = sanitize(f)

        if rc is False:
            failedlist.append(f)

    if len(failedlist) > 0:
        
        for f in failedlist:
            print(f"Failed sanity {f}")

        sys.exit(-1)
    
    sys.exit(0)
