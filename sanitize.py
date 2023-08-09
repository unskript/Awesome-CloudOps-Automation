#!/usr/bin/env python
#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import os
import json
import sys
import argparse


import nbformat
import re
import requests
from collections import defaultdict
from urlextract import URLExtract

def extract_links_from_notebook(notebook_path, extractor):
    with open(notebook_path) as f:
        notebook = nbformat.read(f, as_version=4)

    links = []
    for cell in notebook.cells:
        if cell.cell_type != "markdown":
            continue

        urls = extractor.find_urls(cell.source)
        links.extend(urls)

    return links

def validate_link(link):

    if link in ("unSkript.com", "us.app.unskript.io"):
        return True

    try:
        response = requests.get(link, timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def check_notebooks(notebook_paths, extractor):
    link_cache = {}
    dead_link_report = defaultdict(list)

    for notebook in notebook_paths:
        links = extract_links_from_notebook(notebook, extractor)
        for link in links:
            if link not in link_cache:
                link_cache[link] = validate_link(link)
            if not link_cache[link]:
                dead_link_report[notebook].append(link)

    return dict(dead_link_report)


## returns True is everything is ok 
def check_sanity(ipynbFile: str = '') -> bool:

    rc = True
    with open(ipynbFile) as f:
        nb = json.loads(f.read())

    jsonFile = ipynbFile.replace("ipynb", "json")
    if os.path.exists(jsonFile) is False:
        print(f"Skipping sanity on file ({ipynbFile}) since {jsonFile} is missing")
        return True
     
    with open(jsonFile) as jf:
        jsonData = json.loads(jf.read())

    if nb.get('metadata') is None:
        print("Failed metadata check for notebook")
        rc = False

    if nb.get('metadata').get('execution_data') is None:
        print("Failed execution_data check for notebook")
        rc = False

    exec_data = nb.get('metadata').get('execution_data')
    if len(exec_data) > 2:
        print("Failed execution_data keys check for notebook")
        rc = False

    if exec_data.get('runbook_name') is None:
        print("Failed runbook_name check for notebook")
        rc = False
    
    ## runbook_name should be same as the name in JSON file
    if exec_data.get('runbook_name') != jsonData.get('name'):
        print("Failed runbook_name value check for notebook")
        rc = False

    if nb.get('metadata').get('parameterSchema') is None:
        print("Failed parameters value check for notebook")
        rc = False

    cells = nb.get("cells")
    for cell in cells:

        if cell.get('cell_type') == 'markdown':
            continue

        if cell.get('metadata') is None:
            print("Failed metadata check for cell")
            rc = False

        if cell.get('metadata').get('tags') is None:
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

        # Look for this pattern
        # "task.configure(credentialsJson='''{\n",
        # "    \"credential_name\": abc,
        # "    \"credential_type\": def",
        # "    \"credential_id\": ghi",
        # "}''')\n",

        # This pattern is ok
        # "task.configure(credentialsJson='''{\"credential_type\": \"" + md.action_type + "\",}''')"

        if cell.get('metadata').get('legotype') is None:
            continue

        action_type = cell.get('metadata').get('legotype').replace("LEGO", "CONNECTOR")
        skip_pattern = 'task.configure(credentialsJson='
        ok_pattern = "task.configure(credentialsJson='''{\\\"credential_type\\\": \\\"" + action_type + "\\\",}''')"
        for line in cell.get('source'):
            if skip_pattern in line and ok_pattern not in line:
                print(f"Failed credentialsJson/code check for cell {cell.get('metadata').get('name')}")
                rc = False

    return rc

def replace_default_string_values_with_extra_quotes(inputDict: dict)-> dict:
    for k, v in inputDict.get('properties').items():
        if 'default' in v.keys():
            if v.get('type') != 'string':
                continue

            defaultValue = v.get('default')
            if defaultValue.startswith("\"") and defaultValue.endswith("\""):
                continue

            if len(defaultValue) > 0:
                newDefaultValue = "\"" + defaultValue + "\""
                v['default'] = newDefaultValue
    return inputDict

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

        cell_type = cell.get('cell_type')
        if cell_type != 'code':
            new_cells.append(cell)
            continue

        if cell.get('metadata').get('legotype') is None:
            print(f"Skipping cell without legotype {cell.get('metadata').get('name')}")
            new_cells.append(cell)
            continue

        # Lets make sure Cell Metadata has tags, only then check if it matches the first cell
        if cell.get('metadata').get('tags') and 'unSkript:nbParam' in cell.get('metadata').get('tags'):
            print("SKIPPING FIRST CELL")
            continue

        if cell.get('metadata').get('inputschema') is not None:
            cell['metadata']['inputschema'] = \
                [ replace_default_string_values_with_extra_quotes(cell.get('metadata').get('inputschema')[0]) ]

        # Reset CredentialsJson
        cell['metadata']['credentialsJson'] = {}

        # Cleanout output
        cell['outputs'] = []

        # Delete CredentialsJson from source
        skip_pattern = "task.configure(credentialsJson="
        action_type = cell.get('metadata').get('legotype').replace("LEGO", "CONNECTOR")
        new_creds_line = "task.configure(credentialsJson='''{\\\"credential_type\\\": \\\"" + action_type + "\\\"}''')"

        cell_source = []
        skip = False
        for line in cell.get('source'):
            if skip_pattern in line and new_creds_line not in line:
                cell_source.append(new_creds_line)
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

    except Exception as e:
        raise e

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
    filelist = []
    for f in args.files:
        # To handle file delete case, check if the file exists.
        if os.path.isfile(f) is False:
            continue

        if f.endswith('.ipynb') is False:
            continue

        filelist.append(f)

    failedlist = []
    print('List of files:', filelist)

    for f in filelist:
        # To handle file delete case, check if the file exists.
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


    extractor = URLExtract()
    dead_links = check_notebooks(filelist, extractor)
    failedlist = []
    for notebook, links in dead_links.items():
        if len(links) == 0:
            continue

        failedlist.append(f)
        print(f'Notebook {notebook} contains the following dead links:')
        for link in links:
            print(link)


    if len(failedlist) > 0:
        
        for f in failedlist:
            print(f"Failed sanity {f}")

        sys.exit(-1)

    sys.exit(0)

## handle uniform region, namespace