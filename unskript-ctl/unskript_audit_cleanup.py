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
import yaml
import ZODB
import datetime
import ZODB.FileStorage
from ZODB import DB

from unskript_utils import *


def remove_old_ipynb_files():
    # Read the Audit period from config file
    audit_period = get_audit_period()
    current_date = datetime.datetime.now()
    threshold_date = current_date - datetime.timedelta(days=audit_period)
    files_deleted = False
    for ipynb_file in os.listdir(UNSKRIPT_EXECUTION_DIR):
        if ipynb_file.endswith('.ipynb'):
            file_path = os.path.join(UNSKRIPT_EXECUTION_DIR, ipynb_file)
            file_ts = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_ts < threshold_date:
                try:
                    os.remove(file_path)
                    print(f"Deleted {file_path}")
                    files_deleted = True
                except Exception as e:
                    print(f"ERROR: {e}")
                    return 

    if files_deleted:
        print(f"Deleted ipynb files older than {audit_period} days!")
    else:
        print(f"No ipynb files are older than {audit_period}. Nothing to delete")
    return

def get_audit_period():
    audit_period = 90
    try:
        if os.path.exists(GLOBAL_CTL_CONFIG) is True:
            with open(GLOBAL_CTL_CONFIG, 'r', encoding='utf-8') as f:
                data = yaml.safeload(f.read())
                if data and data.get('global') and data.get('global').get('audit_period'):
                    audit_period = data.get('global').get('audit_period')
    except:
        # We use 90 days as the default period to cleanup  then.
        pass 
    return audit_period


def clean_db() -> DB:
    """clean_db This function calls the db.pack(...) function to cleanup the ZoDB of data that are audit_period old
       default is 90 days. This function can be called as docker cron job to cleanup ZoDB data that are 90 days old
    """
    audit_period = get_audit_period()

    try:
        db = DB(PSS_DB_PATH)
        db.pack(days=audit_period)
        db.close()
        print("Clean up successful")
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == '__main__':
    remove_old_ipynb_files()
    clean_db()