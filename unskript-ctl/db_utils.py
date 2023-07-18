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
            list_checks.append([s_connector.capitalize(), d.get('name'), d.get('uuid')])
        else:
            list_checks.append(d)

    tm.commit()
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
