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

# Global Constants used in this file
# GLOBAL_UNSKRIPT_CONFIG_FILE = '/unskript/etc/unskript_global.yaml'
GLOBAL_UNSKRIPT_CONFIG_FILE = './unskript_global.yaml'


def unskript_ctl_config_smtp(args):
    pass 

def unskript_ctl_unconfig_smtp(args):
    pass 


def unskript_ctl_config_slack(args):
    pass 

def unskript_ctl_unconfig_slack(args):
    pass 

def unskript_ctl_config_create_notification(type, creds_data):
    if not type or not creds_data:
        print("ERROR: Type & creds_data are mandatory parameters for this function")
        return
    
    data = {}
    data['notification'] = {}
    if type == 'slack':
        data['notification']['type'] = 'slack'
        data['notification']['slack'] = {}
        data['notification']['slack']['creds'] = {}
        if isinstance(creds_data, str) is False:
            print("ERROR: Webhook Should be of type String")
            return
        data['notification']['slack']['creds']['hook_url'] = creds_data
    elif type == 'mail':
        data['notification']['type'] = 'mail'
        data['notification']['mail'] = {}
        data['notification']['mail']['creds'] = {}
        if isinstance(creds_data, dict):
            if list(creds_data.keys()).sort() != ['smtp_user', 'smtp_host', 'smtp_password'].sort():
                print(f"ERROR: Creds Data should have smtp_user, smtp_host and smtp_password Keys!")
                return

            for k, v in creds_data.items():
                data['notification']['mail']['creds'][k] = v
        else:
            print(f"ERROR: Creds_Data should be of type dictionary")
            return
    else:
        print(f"ERROR: Option {type} is not implemented")
        return
    
    existing_data = {}
    if os.path.exists(GLOBAL_UNSKRIPT_CONFIG_FILE) is True:
        with open(GLOBAL_UNSKRIPT_CONFIG_FILE, 'r', encoding='utf-8') as f:
            existing_data = yaml.safe_load(f.read())

    existing_data['notification'] = data['notification']
    
    with open(GLOBAL_UNSKRIPT_CONFIG_FILE, 'w', encoding='utf-8') as f:
        f.write(yaml.safe_dump(existing_data))
    
    print("Successfully Registered Notification Entry in Global Configuration")


def unskript_ctl_config_read_notification(type):
    if not type:
        print("ERROR: Type is mandatory parameters for this function")
        return
        
    existing_data = {}
    if os.path.exists(GLOBAL_UNSKRIPT_CONFIG_FILE) is True:
        with open(GLOBAL_UNSKRIPT_CONFIG_FILE, 'r', encoding='utf-8') as f:
            existing_data = yaml.safe_load(f.read())

    if existing_data['notification'].get(type):
        return existing_data
    else:
        print(f"ERROR: No saved Data of {type}? Please check if it was configured")
        return None 
    
def unskript_ctl_config_update_notification(type, creds_data):
    if not type or not creds_data:
        print("ERROR: Type & creds_data are mandatory parameters for this function")
        return
    
    data = {}
    data['notification'] = {}
    if type == 'slack':
        data['notification']['type'] = 'slack'
        data['notification']['slack'] = {}
        data['notification']['slack']['creds'] = {}
        if isinstance(creds_data, str) is False:
            print("ERROR: Webhook Should be of type String")
            return
        data['notification']['slack']['creds']['hook_url'] = creds_data
    elif type == 'mail':
        data['notification']['type'] = 'mail'
        data['notification']['mail'] = {}
        data['notification']['mail']['creds'] = {}
        if isinstance(creds_data, dict):
            if list(creds_data.keys()).sort() != ['smtp_user', 'smtp_host', 'smtp_password'].sort():
                print(f"ERROR: Creds Data should have smtp_user, smtp_host and smtp_password Keys!")
                return

            for k, v in creds_data.items():
                data['notification']['mail']['creds'][k] = v
        else:
            print(f"ERROR: Creds_Data should be of type dictionary")
            return
    else:
        print(f"ERROR: Option {type} is not implemented")
        return
    
    existing_data = {}
    if os.path.exists(GLOBAL_UNSKRIPT_CONFIG_FILE) is True:
        with open(GLOBAL_UNSKRIPT_CONFIG_FILE, 'r', encoding='utf-8') as f:
            existing_data = yaml.safe_load(f.read())

    existing_data['notification'] = data['notification']
    
    with open(GLOBAL_UNSKRIPT_CONFIG_FILE, 'w', encoding='utf-8') as f:
        f.write(yaml.safe_dump(existing_data))
    
    print("Successfully Updated Notification Entry in Global Configuration")

def unskript_ctl_config_delete_notification(type):
    if not type:
        print("ERROR: Type is mandatory parameters for this function")
        return
        
    existing_data = {}
    if os.path.exists(GLOBAL_UNSKRIPT_CONFIG_FILE) is True:
        with open(GLOBAL_UNSKRIPT_CONFIG_FILE, 'r', encoding='utf-8') as f:
            existing_data = yaml.safe_load(f.read())

    if existing_data['notification'].get('type') == type:
        del existing_data['notification']
        with open(GLOBAL_UNSKRIPT_CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write(yaml.safe_dump(existing_data))    
    else:
        print(f"ERROR: No saved Data of {type}? Nothing to delete")
        return None


def unskript_ctl_create_schedule(args):
    pass 

def unskript_ctl_read_schedule(args):
    pass 

def unskript_ctl_update_schedule(args):
    pass 

def unskript_ctl_delete_schedule(args):
    pass 

