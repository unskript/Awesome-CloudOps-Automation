#!/usr/bin/env python
#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
#
import glob
import os
import importlib

def get_py_files() -> list:
    """ get_py_files finds out all the python files under each `CONNECTOR/legos`
        directory and returns this a s list. We use glob.glob() to search through
        all Connectors using the wildcard `**`. The file list is then filtered
        to exclude __init__.py and return the actual python files.

        :rtype: list, the list of python files
    """
    f = glob.glob('./**/legos/*/*.py')
    f = [x for x in f if os.path.basename(x) != '__init__.py']
    return f

def test_if_importable(files: list) -> bool:
    """ test_if_importable is a function that just does what it says. For the given
        python file, it does a equivalent of `from <CONNECTOR>.legos.<LEGO_DIR>.<LEGO_NAME> import *`
        if there was any mistake in the code, the import will catch it and let us know
        any syntactical issues. This code does not check any business logic. Only does
        make sure that syntactical errors are not introduced.

        :type files: list
        :param files: List of python files that need to be checked for imports

        :rtype: bool, True if importable, False if files is empty or not a list.
                Exception in case not able to import the file
    """
    if not files or not isinstance(files, list):
        return False 
    
    print(f"Total number of file: {len(files)}")
    for f in files:
        print(f"Processing {f} ...")
        # Remove Leading `./`
        f = f.replace('./', '')
        # Replace `/` with `.`
        f = f.replace('/', '.')
        # Remove trailing `.py`
        f = f.replace('.py', '')
        try:
            module = importlib.import_module(f)
            globals().update(vars(module))
        except ValueError as e:
            print(f"ERROR IMPORTING: {f}")
            raise e
    return True

if __name__ == '__main__':
    files = get_py_files()
    result = test_if_importable(files)
    if result:
        print(f"Success: All python files import cleanly")
    else:
        print(f"ERROR. Issue with importing some libraries, check console output")
