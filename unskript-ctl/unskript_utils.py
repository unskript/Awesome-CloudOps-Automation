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
import os
import sys 

from datetime import datetime 

UNSKRIPT_EXECUTION_DIR="/unskript/data/execution/"
PSS_DB_PATH="/unskript/db/unskript_pss.db"
GLOBAL_CTL_CONFIG="/etc/unskript/unskript_ctl_config.yaml"
CREDENTIAL_DIR="/.local/share/jupyter/metadata/credential-save"

UNSKRIPT_SCRIPT_RUN_OUTPUT_FILE_NAME = "unskript_script_run_output"
UNSKRIPT_SCRIPT_RUN_OUTPUT_DIR_ENV = "UNSKRIPT_SCRIPT_OUTPUT_DIR"
JIT_PYTHON_SCRIPT = "/tmp/jit_script.py"

TBL_HDR_CHKS_NAME="\033[36m Checks Name \033[0m"
TBL_HDR_DSPL_CHKS_NAME="\033[35m Check Name \n (Last Failed) \033[0m"
TBL_HDR_DSPL_EXEC_ID="\033[1m Failed Execution ID \033[0m"
TBL_HDR_FAILED_OBJECTS="\033[1m Failed Objects \033[0m"
TBL_HDR_CHKS_FN="\033[1m Function Name \033[0m"
TBL_HDR_LIST_CHKS_CONNECTOR="\033[36m Connector Name \033[0m"


CONNECTOR_LIST = [
    'aws', 
    'gcp', 
    'k8s', 
    'elasticsearch', 
    'grafana', 
    'redis', 
    'jenkins', 
    'github', 
    'netbox', 
    'nomad', 
    'jira', 
    'kafka', 
    'mongodb', 
    'mysql', 
    'postgresql', 
    'rest', 
    'slack', 
    'ssh', 
    'vault',
    'salesforce'
]

# Unskript Global is a singleton class that
# will replace the Global variable UNSKRIPT_GLOBAL
# It becomes essential to use this class to keep the spread of 
# Variable to a minimum and access it every where within the scope
# of the program

class GenericSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(GenericSingleton, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class UnskriptGlobals(metaclass=GenericSingleton):
    def __init__(self):
        self._data = {}

    def __getitem__(self, key):
        return self._data.get(key, None)

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def get(self, key):
        return self._data.get(key, None)
    
    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def create_property(self, prop_name):
        def getter(self):
            return self._data.get(prop_name, None)

        def setter(self, value):
            self._data[prop_name] = value

        setattr(UnskriptGlobals, prop_name, property(getter, setter))



# Lets create an Alias so that any reference to UNSKRIPT_GLOBAL
# refers to the class. In this way no change has to be done
# when UNSKRIPT_GLOBALS variable is used. 
UNSKRIPT_GLOBALS = UnskriptGlobals()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ARG_START = '\x1B[1;20;42m'
    ARG_END = '\x1B[0m'

# Utility Functions
def create_execution_run_directory(file_prefix: str = None):
    if UNSKRIPT_GLOBALS.get('CURRENT_EXECUTION_RUN_DIRECTORY') is None:
        current_time = datetime.now().isoformat().replace(':', '_')
        if not file_prefix:
            output_dir = UNSKRIPT_EXECUTION_DIR + f"{UNSKRIPT_SCRIPT_RUN_OUTPUT_FILE_NAME}-{current_time}"
        else:
            output_dir = UNSKRIPT_EXECUTION_DIR +  f"{file_prefix}-{current_time}"

        try:
            os.makedirs(output_dir)
        except Exception as e:
            print(f'{bcolors.FAIL} output dir {output_dir} creation failed{bcolors.ENDC}')
            sys.exit(0)
        finally:
            UNSKRIPT_GLOBALS.create_property('CURRENT_EXECUTION_RUN_DIRECTORY')
            UNSKRIPT_GLOBALS['CURRENT_EXECUTION_RUN_DIRECTORY'] = output_dir
    else:
        output_dir = UNSKRIPT_GLOBALS.get('CURRENT_EXECUTION_RUN_DIRECTORY')    
    return output_dir