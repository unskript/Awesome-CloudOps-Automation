#!/usr/bin/env python
#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE
#
#

import os
import sys
import transaction
import time
import json
import re 

import ZODB, ZODB.FileStorage
from ZODB import DB

try:
    sys.path.append(f"/usr/share/unskript")
    from unskript_db_utils import PssDB, CodeSnippetsDB
except Exception as e:
    raise e

"""
Utility function that will be used in the unskript-client for DB
access. The utility functions uses ZoDB. 
"""

"""
LIST OF CONSTANTS USED IN THIS FILE
"""


def upsert_pss_record(name: str, data: dict, overwrite: bool=False):
    """upsert_pss_record This function creates/updates db record with the
       given name with the data given.

       :type name: string
       :param name: Key name, with which the record should be created
                    example: failed_checks
     
       :type data:  dictionary
       :param data: The data in the form in the python  dictionary

       :type overwrite: boolean
       :param overwrite: Flag to overwrite existing data, default is false.
              if True, the Data will be appeneded as a list of dictionaries 
              to the key specified by name.

       :rtype: None in case of success or Error
    """
    if name in ("", None):
        raise Exception("Name cannot be Empty")
    
    if isinstance(data, dict) != True:
        raise Exception(f"Data is expected to be of type Dictionary type, found {type(data)}")
    
    db = PssDB()
    db_data = []
    if name == 'audit_trail':
        key = [x for x in data.keys()][0]
        k = str(key.urn.split(':')[-1])
        db_data.append(k)
        db_data.append(data[key].get('time_stamp'))
        check_id = [x for x in data[key].get('check_status').keys()][0]
        db_data.append(check_id)
        db_data.append(data[key]['check_status'][check_id].get('check_name'))
        db_data.append(data[key]['check_status'][check_id].get('status'))
        db_data.append(data[key]['check_status'][check_id].get('connector'))
        db_data.append(data[key].get('summary'))
    elif name == 'default_credential':
        for k,v in data.items():
            t = []
            t.append(k)
            t.append(data[k].get('name')) 
            t.append(data[k].get('id'))
            db.insert_or_replace(name, t)
        return
    elif name == 'current_execution_status':
        check_id = [x for x in data.get('exec_status').keys()][0]
        db_data.append(check_id)
        db_data.append(data['exec_status'][check_id].get('failed_runbook'))
        db_data.append(data['exec_status'][check_id].get('check_name'))
        db_data.append(data['exec_status'][check_id].get('current_status'))
        db_data.append(data['exec_status'][check_id].get('connector_type'))
        db_data.append(data['exec_status'][check_id].get('passed_timestamp'))
        db_data.append(data['exec_status'][check_id].get('failed_timestamp'))
    elif name == 'check_run_trail':
        check_id = [x for x in data.keys()][0]
        db_data.append(check_id)
        db_data.append(data[check_id].get('time_stamp'))
        db_data.append(data[check_id].get('check_name'))
        db_data.append(data[check_id].get('connector_type'))
        db_data.append(data[check_id].get('status'))
        db_data.append(data[check_id].get('failed_objects'))
        
    db.insert_or_replace(name, db_data)


def get_pss_record(name: str):
    """get_pss_record This function queries the ZoDB for the given
       record stored by name and either returns the complete record
       or the last item in the list.

       :type name: string
       :param name: Name of the record (Key name in the DB)
    
       :rtype: record saved with the  name or None
    """

    if name in ("", None):
        print(f"ERROR: Name cannot be empty")
        return {} 
    
    data = {}
    db = PssDB()
    cur = db.cursor()
    result = cur.execute(f"SELECT * FROM {name}")
    if name == 'audit_trail':
        for r in result: 
            temp_data = {}
            exec_id = r[0]
            check_id = r[2]
            temp_data[exec_id] = {}
            temp_data[exec_id]['time_stamp'] = r[1]
            temp_data[exec_id]['check_status'] = {}
            temp_data[exec_id]['check_status'][check_id] = {}
            temp_data[exec_id]['check_status'][check_id]['status'] = r[4]
            temp_data[exec_id]['check_status'][check_id]['connector'] = r[5]
            temp_data[exec_id]['summary'] = r[6]
            data.update(temp_data)
    elif name == 'default_credential':
        for r in result:
            temp_data = {}
            type = r[0]
            temp_data[type] = {}
            temp_data[type]['name'] = r[1]
            temp_data[type]['id'] = r[2]
            data.update(temp_data)
    elif name == 'check_run_trail':
        for r in result:
            temp_data = {}
            check_id = r[0]
            temp_data[check_id] = {}
            temp_data[check_id]['time_stamp'] = r[1]
            temp_data[check_id]['action_uuid'] = check_id 
            temp_data[check_id]['check_name'] = r[2] 
            temp_data[check_id]['connector_type'] = r[3] 
            temp_data[check_id]['status'] = r[4] 
            temp_data[check_id]['failed_objects'] = r[5]
            data.update(temp_data)
    elif name == 'current_execution_status':
        for r in result:
            temp_data = {}
            check_id = r[0]
            temp_data['exec_status'] = {}
            temp_data['exec_status'][check_id] = {}
            temp_data['exec_status'][check_id]['failed_runbook'] = r[1]
            temp_data['exec_status'][check_id]['check_name'] = r[2]
            temp_data['exec_status'][check_id]['current_status'] = r[3]
            temp_data['exec_status'][check_id]['connector_type'] = r[4]
            temp_data['exec_status'][check_id]['passed_timestamp'] = r[5]
            temp_data['exec_status'][check_id]['failed_timestamp'] = r[6]
            data.update(temp_data)
    else:
        pass
             
    if not data:
        print(f"ERROR: No records found by the name {name}")
        return {}

    return data


def get_checks_by_connector(connector_name: str, full_snippet: bool = False):
    """get_checks_by_connector This function queries the snippets DB for
       checks of type connect and returns the checks.

       :type connector_name: string
       :param connector_name: Name of the connector 

       :rtype: List of the checks 
    """
    list_check = []
    db = CodeSnippetsDB()
    cur = db.cursor()
    if connector_name.lower() == 'all':
        query = f"SELECT * FROM snippets;"
    else:
        c_name = "LEGO_TYPE_" + connector_name.upper() + "*"
        #query = f"SELECT * FROM snippets WHERE type = \"{c_name}\";"
        query = f"SELECT * FROM snippets WHERE type GLOB \"{c_name}\";"
        print(f"QUERY is {query}")
    
    # FOR FUTURE USE
    all_lego_result = cur.execute(query)

    all_check_result = []
    for r in all_lego_result:
        # Lets filter all checks legos
        data = r[-1] 
        data_dict = json.loads(data)
        if data_dict.get('metadata').get('action_is_check') == True:
            all_check_result.append(r)

     
    for r in all_check_result:
        if full_snippet:
            data = r[-1]
            data_dict = json.loads(data)
            list_check.append(data_dict)
        else:
            c_name = r[2]
            c_name = c_name.replace('LEGO_TYPE_', '')
            list_check.append([c_name.upper(), r[0], r[3]])

    return list_check

def get_creds_by_connector(connector_type: str):
    """get_creds_by_connector This function queries ZoDB and returns the
    credential data in the form of a tuple of (cred_name, cred_id).

    :type connector_type: string
    :param connector_type: Connector Type like CONNECTOR_TYPE_AWS, etc..
    
    :rtype: Tuple (cred_name, cred_id)
    """
    retval = ()

    if connector_type is ('', None):
        return retval
    
    creds_dict = get_pss_record('default_credential')
    if not creds_dict:
        return retval 
    
    for cred in creds_dict.keys():
        if cred == connector_type: 
            retval = (creds_dict.get(cred).get('name'), creds_dict.get(cred).get('id'))

    return retval
