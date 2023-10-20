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

import yaml
import os

from pathlib import Path 

try:
    from envyaml import EnvYAML
except Exception as e:
    print("ERROR: Unable to find required yaml package to parse the config file")
    raise e

# Global Constants used in this file
GLOBAL_UNSKRIPT_CONFIG_FILE = '/unskript/etc/unskript_ctl_config.yaml'


def unskript_ctl_config_read_notification(n_type: str):
    """unskript_ctl_config_read_notification: This is the Read notification. This function reads the configuration
    and returns the Notification configuration as a python dictionary. This is the Read function of Notification.
    """
    if not n_type:
        print("ERROR: Type is mandatory parameters for this function")
        return

        
    existing_data = {}
    if os.path.exists(GLOBAL_UNSKRIPT_CONFIG_FILE) is True:
        existing_data = EnvYAML(GLOBAL_UNSKRIPT_CONFIG_FILE, strict=False)

    n_dict = existing_data.get('notification')
    if not n_dict:
        print("ERROR: No Notification data found")
        return

    if n_dict.get(n_type):
        if n_type.lower() == 'email':
            if n_dict.get('Email').get('enable') is True:
                notify_data = n_dict.get('Email')
                return notify_data
            else:
                print("ERROR: Enable flag under Email section is set to false, please change to true and re-run")
                return {}
        elif n_type.lower() == 'slack':
            if n_dict.get('Slack').get('enable') is True:
                return n_dict.get('Slack')
            else:
                print("ERROR: Enable flag under Slack section is set to false, please change to true and re-run")
                return {}
        else:
            print(f"ERROR: Opton {n_type} is not supported")
            return {}
    else:
        print(f"No Notification found for {n_type}")
        return {} 