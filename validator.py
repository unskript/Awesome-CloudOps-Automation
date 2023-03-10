#!/usr/bin/env python
#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
#
import os
import json 
import glob 
import sys 
import time 

from subprocess import run

def git_top_dir() -> str:
    """git_top_dir returns the output of git rev-parse --show-toplevel 

    :rtype: string, the output of the git rev-parse --show-toplevel comand
    """
    run_output = run(["git", "rev-parse", "--show-toplevel"], capture_output=True)
    top_dir = run_output.stdout.strip()
    top_dir = top_dir.decode('utf-8')
    return top_dir 

def check_action_by_connector_names(connector: str = '') -> bool:
    """check_action_by_connector_names This function takes the connector name and
       verifies if the contents under the <connector>/legos/<lego_for_connector>/ 
       has the same name. For examples AWS/legos/aws_check_expired_keys 
       should have the following contents.
       AWS/legos/aws_check_expired_keys 
               + aws_check_expired_keys.py
               + aws_check_expired_keys.json
               + README.md
               + __init__.py 
               + (Optional) 1.png (Sample output screenshot)
    
       :type connector: string
       :param connector: The Connector name that the Action is written for. 

       :rtype: bool (T/F) True if validate passes, False otherwise.
    """
    if connector == '':
        return False

    top_dir = git_top_dir()
    dirs_under_connector = [] 
    if top_dir not in ('', None):
        dirs_under_connector = os.listdir(os.path.join(top_dir, connector, 'legos'))
    
    if len(dirs_under_connector) == 0:
        print(f"ERROR: No contents found under {connector}")
        return False
    
    process_list = []
    m = Manager()
    ret_val = m.dict()
    #  Spawn multiple process to verify for parallel processing
    #  Lets batch it and process it for every 20 
    idx = 0
    print(f"CONNECTOR {connector} ({len(dirs_under_connector)})")
    for _dir in dirs_under_connector:
        if _dir in ('templates', '__init__.py'):
            continue 
        check_dir_contents(os.path.join(connector, 'legos', _dir), ret_val)

    for k,v in ret_val.items():
        if v == False:
            print(f"CHECK FAILED FOR {k}")
            return False
    
    return True

def check_dir_contents(_dir: str, ret_val) -> bool:
    """check_dir_contents This is a worker function that goes into each of
       the given directory and checks the following.
       1. Name of python file  and json file should be the directory name with .py and .json extension
       2. action_entry_function should be the same as directory name in the json file
       3. README.md and __init__.py should be present in the given directory
       
       If all the above case are met, the function returns True, else False

       :type _dir: string
       :param _dir: Name of the directory

       :rtype: bool. True if all the check pass, Flase otherwise
    """
    dir_content = glob.glob(os.path.join(_dir, '*'))
    if len(dir_content) < 4:
        return False

    pyfile = os.path.join(_dir, os.path.basename(_dir) + '.py')
    jsonfile = os.path.join(_dir, os.path.basename(_dir) + '.json')
    readmefile = os.path.join(_dir, 'README.md')
    initfile = os.path.join(_dir,'__init__.py')
    if pyfile not in dir_content \
        or jsonfile not in dir_content \
        or initfile not in dir_content \
        or readmefile not in dir_content:
        ret_val[_dir] = False
        print(f"ERROR: Missing File {dir_content} ")
        return
    
    try:
        with open(jsonfile, 'r') as f:
            d = json.load(f)

        if d.get('action_entry_function') != os.path.basename(_dir):
            print(f"ERROR: ENTRY FUNCTION IN {jsonfile} is Wrong Expecting: {os.path.basename(_dir)} Has: {d.get('action_entry_function')}")
            ret_val[_dir] = False
            return 
    except Exception as e:
        ret_val[_dir] = False
        raise e
 
    ret_val[_dir] = True
    return


def main():
    """main: Main function that gets called. This function finds out all Legos directories
       and calls the check_action_by_connector_name for each of the connectors.
    """
    all_connectors = glob.glob(git_top_dir() + '/*/legos')
    result = []
    for connector in all_connectors:
        connector = connector.replace(git_top_dir() + '/', '')
        result.append(check_action_by_connector_names(os.path.dirname(connector)))
    
    for r in result:
        if r == False:
            print("ERROR: Check Failed. Please note the Validation process checks -")
            print("ERROR:     1. Lego Directory name should match python and json file name ") 
            print("ERROR:     2. Action Entry function should be the same as Lego directory name") 
            print("ERROR:     3. A __init__.py File should exist for every Lego directory")
            print("ERROR:     4. A README.md should be present for every Lego")
            print("ERROR:     5. (Optional) A Screen shot that is referenced in README.md that shows output of the Action")
            sys.exit(-1)

    print("Checks were successful")
    return


if __name__ == '__main__':
    main()
