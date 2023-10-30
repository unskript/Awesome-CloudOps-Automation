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
import ZODB.FileStorage
from ZODB import DB

# LIST OF CONSTANTS USED IN THIS FILE

PSS_DB_PATH="/unskript/db/unskript_pss.db"
GLOBAL_CTL_CONFIG="/etc/unskript/unskript_ctl_config.yaml"

def clean_db() -> DB:
    """clean_db This function calls the db.pack(...) function to cleanup the ZoDB of data that are audit_period old
       default is 90 days. This function can be called as docker cron job to cleanup ZoDB data that are 90 days old
    """
    audit_period = 90
    try:
        if os.path.exists(GLOBAL_CTL_CONFIG) == True:
            with open(GLOBAL_CTL_CONFIG, 'r', encoding='utf-8') as f:
                data = yaml.load(f.read())
                if data and data.get('global') and data.get('global').get('audit_period'):
                    audit_period = data.get('global').get('audit_period')
    except:
        # We use 90 days as the default period to cleanup  then.
        pass 

    try:
        db = DB(PSS_DB_PATH)
        db.pack(days=audit_period)
        db.close()
        print("Cleaned up successful")
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == '__main__':
    clean_db()