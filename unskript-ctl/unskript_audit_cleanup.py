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
import shutil
import ZODB
import datetime
import ZODB.FileStorage
from ZODB import DB

from unskript_utils import *


# We also need to remove old directories in the execution directory
# That are older than the threshold date
def remove_old_directories():
    # Read the Audit period from config file
    audit_period = get_audit_period()
    current_date = datetime.datetime.now()
    threshold_date = current_date - datetime.timedelta(days=audit_period)
    directories_deleted = False
    for directory in os.listdir(UNSKRIPT_EXECUTION_DIR):
        dir_path = os.path.join(UNSKRIPT_EXECUTION_DIR, directory)
        if os.path.isdir(dir_path):
            dir_ts = datetime.datetime.fromtimestamp(os.path.getmtime(dir_path))
            if dir_ts < threshold_date:
                try:
                    # Use shutil.rmtree instead of os.rmdir to remove non-empty directories
                    shutil.rmtree(dir_path)
                    print(f"Deleted {dir_path}")
                    directories_deleted = True
                except Exception as e:
                    print(f"ERROR: Failed to delete {dir_path}: {e}")
                    # Continue with other directories rather than returning
                    continue

    if directories_deleted:
        print(f"Deleted directories older than {audit_period} days!")
    else:
        print(f"No directories are older than {audit_period}. Nothing to delete")
    return


def get_audit_period():
    audit_period = 90
    try:
        if os.path.exists(GLOBAL_CTL_CONFIG) is True:
            with open(GLOBAL_CTL_CONFIG, "r", encoding="utf-8") as f:
                data = yaml.safeload(f.read())
                if (
                    data
                    and data.get("global")
                    and data.get("global").get("audit_period")
                ):
                    audit_period = data.get("global").get("audit_period")
    except:
        # We use 90 days as the default period to cleanup  then.
        pass
    return audit_period


def clean_db() -> None:
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


if __name__ == "__main__":
    remove_old_directories()
    clean_db()
