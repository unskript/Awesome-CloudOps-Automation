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
import re
import transaction
import ZODB
import ZODB.FileStorage
from ZODB import DB


# Utility function that will be used in the unskript-client for DB
# access. The utility functions uses ZoDB. 

# LIST OF CONSTANTS USED IN THIS FILE

PSS_DB_DIR="/unskript/db"
PSS_DB_PATH="/unskript/db/unskript_pss.db"
CS_DB_PATH="/var/unskript/snippets.db"
SNIPPETS_FILE="/var/unskript/code_snippets.json"
CUSTOM_SNIPPETS="/unskript/data/custom/custom_snippets.json"

def init_pss_db() -> DB:
    """init_pss_db This function initializes PSS db. 
       :rtype: DB object. 
    """
    if not os.path.exists(PSS_DB_DIR):
        os.mkdir(PSS_DB_DIR)

    if not os.path.exists(PSS_DB_PATH):
        pss = ZODB.FileStorage.FileStorage(PSS_DB_PATH)
        db = DB(pss)

        # connection = db.open()
        # root = connection.root()
        with db.transaction() as connection:
            root = connection.root()
            root['audit_trail'] = {}
            root['default_credential_id'] = {}
            root['check_run_trail'] = {}
            root['current_execution_status'] = {}
            del root
            del connection

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

    if isinstance(data, dict) is not True:
        raise Exception(f"Data is expected to be of type Dictionary type, found {type(data)}")

    db = init_pss_db()
    with db.transaction() as connection: 
        root = connection.root()
        if overwrite:
            root[name] = data
        else:
            d = root[name]
            d.update(data)
            root[name] = d
        del root
        del connection 

    db.close()


def get_pss_record(name: str):
    """get_pss_record This function queries the ZoDB for the given
       record stored by name and either returns the complete record
       or the last item in the list.

       :type name: string
       :param name: Name of the record (Key name in the DB)
    
       :rtype: record saved with the  name or None
    """

    if name in ("", None):
        print("ERROR: Name cannot be empty")
        return {}

    db = init_pss_db()
    data = None
    with db.transaction() as connection:
        root = connection.root()
        data = root.get(name)
        if data is None:
            # If data does not exist, lets create it
            root[name] = {}
        del root

    db.close()

    if data is None:
        print(f"ERROR: No records found by the name {name}")
        return {}

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
        print("ERROR: Record Name and/or Document Name cannot be empty")
        return False

    db = init_pss_db()
    tm = transaction.TransactionManager()
    connection = db.open(tm)
    root = connection.root()

    data = root.get(record_name)
    if data is None:
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

    tm.commit()
    del root
    connection.close()
    return True


def get_checks_by_uuid(check_uuid_list: list):
    """get_checks_by_uuid This function queries the snippets DB for
       checks that match the give UUID and returns the checks.

       :type check_uuid_list: list
       :param check_uuid_list: List of Check UUIDs

       :rtype: List of checks that match uuids
    """
    if not check_uuid_list:
        return None
    
    try:
        db = DB(CS_DB_PATH)
    except Exception as e:
        raise e
    tm = transaction.TransactionManager()
    connection = db.open(tm)
    root = connection.root()
    cs = root.get('unskript_cs')
    list_checks = []
    if cs is None:
        raise Exception("Code Snippets Are missing")
    for s in cs:
        d = s

        if d.get('metadata').get('action_is_check') is False:
            continue
        c_uuid = d.get('uuid')
        if c_uuid and c_uuid in check_uuid_list:
            list_checks.append(d)
    
    tm.commit()
    del root
    connection.close()
    db.close()
    return list_checks


def get_checks_by_connector(connector_name: str, full_snippet: bool = False):
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
    tm = transaction.TransactionManager()
    connection = db.open(tm)
    root = connection.root()
    cs = root.get('unskript_cs')
    list_checks = []
    if cs is None:
        raise Exception("Code Snippets Are missing")
    for s in cs:
        d = s
        s_connector = d.get('metadata').get('action_type')
        s_connector = s_connector.split('_')[-1].lower()

        if d.get('metadata').get('action_is_check') is False:
            continue
        if connector_name.lower() != 'all' and not re.match(connector_name.lower(), s_connector):
            continue
        if full_snippet is False:
            list_checks.append([s_connector.capitalize(), d.get('name'), d.get('metadata').get('action_entry_function')])
        else:
            list_checks.append(d)

    tm.commit()
    del root
    connection.close()
    db.close()
    return list_checks

def get_all_check_names():
    """get_all_check_names This function queries the snippets DB for
       checks and returns the Names

       :rtype: List containing names of all check
    """
    try:
        db = DB(CS_DB_PATH)
    except Exception as e:
        raise e
    tm = transaction.TransactionManager()
    connection = db.open(tm)
    root = connection.root()
    cs = root.get('unskript_cs')
    list_check_names = []
    if cs is None:
        raise Exception("Code Snippets Are missing")
    for s in cs:
        d = s
        if d.get('metadata').get('action_is_check') is False:
            continue
        list_check_names.append(d.get('metadata').get('action_entry_function'))
        

    tm.commit()
    del root
    connection.close()
    db.close()
    return list_check_names

def get_check_by_name(name: str):
    """get_check_by_name This function utilizes the function get_check_by_connector
       with `all` filter and finds out the check that matches the name and returns 
       the code snippet that matches the name.

       :type name: str
       :param name: Check name 

       :rtype: Returns the Check
    """
    all_snippets = get_checks_by_connector('all', True)
    snippet_list = [x for x in all_snippets if x.get('metadata').get('action_entry_function') == name]

    return snippet_list 

def get_creds_by_connector(connector_type: str):
    """get_creds_by_connector This function queries ZoDB and returns the
    credential data in the form of a tuple of (cred_name, cred_id).

    :type connector_type: string
    :param connector_type: Connector Type like CONNECTOR_TYPE_AWS, etc..
    
    :rtype: Tuple (cred_name, cred_id)
    """
    retval = ()

    if connector_type in ('', None):
        return retval

    db = init_pss_db()
    tm = transaction.TransactionManager()
    connection = db.open(tm)
    root = connection.root()
    try:
        creds_dict = root.get('default_credential_id')
    except Exception:
        pass
    if creds_dict is None:
        pass
    else:
        for cred in creds_dict.keys():
            if cred == connector_type:
                retval = (creds_dict.get(cred).get('name'), creds_dict.get(cred).get('id'))
                break
    tm.commit()
    del root
    connection.close()
    db.close()

    if not retval:
        retval = (None, None)

    return retval

