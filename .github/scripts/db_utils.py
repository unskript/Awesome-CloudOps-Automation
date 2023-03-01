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

"""
Utility function that will be used in the unskript-client for DB
access. The utility functions uses ZoDB. 
"""

"""
LIST OF CONSTANTS USED IN THIS FILE
"""
PSS_DB_DIR="/data/db"
PSS_DB_PATH="/data/db/unskript_pss.db"
CS_DB_PATH="/var/unskript/snippets.db"
SNIPPETS_FILE="/var/unskript/code_snippets.json"
CUSTOM_SNIPPETS="/data/custom/custom_snippets.json"


def init_pss_db() -> DB:
    """init_pss_db This function initializes PSS db. 
       :rtype: DB object. 
    """
    if not os.path.exists(PSS_DB_DIR):
        os.mkdir(PSS_DB_DIR)
    
    if not os.path.exists(PSS_DB_PATH):
        pss = ZODB.FileStorage.FileStorage(PSS_DB_PATH)
        db = DB(pss)
    else:
        db = DB(PSS_DB_PATH)
    
    return db


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
        raise Exception(f"Data is expected to be of type Dictionary type, found {type(d)}")
    
    db = init_pss_db()
    connection = db.open()
    root = connection.root()
    if overwrite:
        root[name] = [data]
    else:
        l = []
        if root.get(name) != None:
            # Update case
            l = [root[name]]
        l.append(data)
        root[name] = l 
    transaction.commit()
    del root 
    connection.close()
    db.close() 


def get_pss_record(name: str, latest: bool = False):
    """get_pss_record This function queries the ZoDB for the given
       record stored by name and either returns the complete record
       or the last item in the list.

       :type name: string
       :param name: Name of the record (Key name in the DB)

       :type latest: bool
       :param latest: This indicates if we have to fetch the latest (last updated)
            record or the full record. Default is False
    
       :rtype: record saved with the  name or None
    """
    if name in ("", None):
        print(f"ERROR: Name cannot be empty")
        return [] 
    
    db = init_pss_db()
    connection = db.open()
    root = connection.root()
    
    data = root.get(name)
    if data == None:
        print(f"ERROR: No records found by the name {name}")
        return []
    
    if latest: 
        return data[-1]
    
    transaction.commit()
    del root 
    connection.close()
    return data

def delete_pss_record(record_name: str, document_name: str) -> bool:
    """delete_pss_record This function deletes ZoDB entry by name
       document_name in the record name. The Record Name is the name
       is the collection name where the document_name is stored. 

       :type record_name: string
       :param record_name: Name of Key with which the data was stored on ZoDB

       :type document_name: string
       :param document_name: Document name, which should be delete form the data
              that was saved with the key record_name. 

       :rtype: Boolean
    """
    if record_name in ("", None) or document_name in ("", None):
        print(f"ERROR: Record Name and/or Document Name cannot be empty")
        return False 
    
    db = init_pss_db()
    connection = db.open()
    root = connection.root()
  
    data = root.get(record_name)
    if data == None:
        return False 

    # Data would be list of dictionaries. 
    # Lets iterate over the list to find the matching key and delete it
    after_delete_data = []
    for d in data:
        for k in d.keys():
            if k == document_name:
                pass
            else:
                after_delete_data.append(d)
    
    root[record_name] = after_delete_data
    
    transaction.commit()
    del root 
    connection.close()
    return True 


def get_checks_by_connector(connector_name: str):
    """get_checks_by_connector This function queries the snippets DB for
       checks of type connect and returns the checks.

       :type connector_name: string
       :param connector_name: Name of the connector 

       :rtype: List of the checks 
    """
    try:
        db = DB(CS_DB_PATH)
    except Exception as e:
        raise e 
    connection = db.open()
    root = connection.root()
    cs = root.get('unskript_cs')
    list_checks = []
    if cs == None:
        raise Exception("Code Snippets Are missing")
    for s in cs:
        d = s.snippet
        s_connector = d.get('metadata').get('action_type')
        s_connector = s_connector.split('_')[-1].lower()
        if connector_name.lower() == 'all':
            if d.get('metadata').get('action_is_check') == True:
                list_checks.append([s_connector.capitalize(), d.get('name'), d.get('uuid')])
        elif re.match(connector_name.lower(), s_connector):
            if d.get('metadata').get('action_is_check') == True:
                list_checks.append([s_connector.capitalize(), d.get('name'), d.get('uuid')])
        else:
            pass

    transaction.commit()
    del root 
    connection.close()
    db.close()
    return list_checks


def get_check_snippets(connector_name: str):
    """get_check_snippets This function queries the snippets DB for
       checks of type connect and returns the checks.

       :type connector_name: string
       :param connector_name: Name of the connector 

       :rtype: List of the checks 
    """
    try:
        db = DB(CS_DB_PATH)
    except Exception as e:
        raise e 
    connection = db.open()
    root = connection.root()
    cs = root.get('unskript_cs')
    list_checks = []
    if cs == None:
        raise Exception("Code Snippets Are missing")
    for s in cs:
        d = s.snippet
        s_connector = d.get('metadata').get('action_type')
        s_connector = s_connector.split('_')[-1].lower()
        if connector_name.lower() == 'all':
            if d.get('metadata').get('action_is_check') == True:
                list_checks.append(d)
        elif re.match(connector_name.lower(), s_connector):
            if d.get('metadata').get('action_is_check') == True:
                list_checks.append(d)
        else:
            pass

    transaction.commit()
    del root 
    connection.close()
    db.close()
    return list_checks

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
    
    try:
        db = DB(CS_DB_PATH)
    except Exception as e:
        raise e 
    tm = transaction.TransactionManager()
    connection = db.open(tm)
    root = connection.root()
    creds_list = root.get('default_credential_id')
    #creds_list = get_pss_record('default_credential_id')
    creds_dict = creds_list[0]
    for cred in creds_dict.keys():
        
        if cred == connector_type: 
            retval = (creds_dict.get(cred).get('name'), creds_dict.get(cred).get('id'))
            break
    
    tm.commit()
    del root 
    connection.close()
    db.close()
    return retval
