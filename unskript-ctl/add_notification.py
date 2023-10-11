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
import json
from pathlib import Path
import subprocess

from argparse import ArgumentParser, REMAINDER
from unskript_ctl_config import *


# GLOBAL CONFIG PATH
if os.environ.get('GLOBAL_CONFIG_PATH') is None:
    GLOBAL_CONFIG_PATH="/unskript/etc/unskript_global.yaml"


# Migrate any existing unskript_config.yaml to unskript_global.yaml
# Note, the earlier name we used was unskript_config.yaml. 
if os.path.exists('/unskript/data/action/unskript_config.yaml') is True:
    try:
        os.makedirs(Path(GLOBAL_CONFIG_PATH).parent, exist_ok=True)
        Path('/unskript/data/action/unskript_config.yaml').rename(GLOBAL_CONFIG_PATH)
    except:
        pass


"""
This class define basic parser that shall be extended based on each notification
type. 
"""
class Notification():
    def __init__(self):
        main_parser = ArgumentParser(prog='add_notification')
        description = ""
        description = description + str("\n")
        description = description + str("\t  Add Notifiction to unSkript-ctl \n")
        main_parser.description = description
        main_parser.add_argument('-c', '--create-notification', choices=[
            'Slack',
            'SMTP'], help='Create Notification')
        main_parser.add_argument('-d', '--delete-notification', choices=[
            'Slack',
            'SMTP'], help='Delete Notification' )
        main_parser.add_argument('-u', '--update-notification', choices=[
            'Slack',
            'SMTP'], help='Update Notification' )
        main_parser.add_argument('-r', '--read-notification', choices=[
            'Slack',
            'SMTP'], help='Read Configured Notification' )
        args = main_parser.parse_args(sys.argv[1:3])
        if len(sys.argv) == 1:
            main_parser.print_help()
            sys.exit(0)
        if args.create_notification not in ('',  None):
            getattr(self, args.create_notification)()
        elif args.delete_notification not in ('', None):
            self.delete_notification(args.delete_notification)
        elif args.update_notification not in ('', None):
            self.update_notification(args.update_notification)
        elif args.read_notification not in ('', None):
            self.read_notification(args.read_notification)
        else:
            print("ERROR: Option not implemented")
            sys.exit(0)
     


    def Slack(self):
        """Slack: This function implements the sub-parser for Slack Notification
        """
        parser = ArgumentParser(description="Add Slack Notification")
        parser.add_argument('-u',
                            '--web-hook-url',
                            required=True,
                            help="Slack Notification Webhook URL")
        parser.add_argument('-c',
                            '--channel-name',
                            required=True,
                            help="Channel Name to send Notification")
        args = parser.parse_args(sys.argv[3:])
        if len(sys.argv[3:]) != 4:
            parser.print_help()
            sys.exit(0)
        
        data = {'hook_url' : args.web_hook_url, 'channel': args.channel_name}
        unskript_ctl_config_create_notification('slack', data) 
    
    def SMTP(self):
        """SMTP: This function implements the sub-parser for Mail/SMTP Notification
        """
        parser = ArgumentParser(description="Add Mail Notification")
        parser.add_argument('-s',
                            '--smtp-host',
                            required=True,
                            help="SMTP Hostname like smtp.google.com")
        parser.add_argument('-u',
                            '--smtp-user',
                            required=True,
                            help="SMTP Username like user@domain.com")
        parser.add_argument('-p',
                            '--smtp-password',
                            required=True,
                            help="SMTP Password for the above user")
        parser.add_argument('-t',
                            '--to-email',
                            required=True,
                            help="Reciever Email address like reciever@example.com")
        args = parser.parse_args(sys.argv[3:])
        if len(sys.argv[3:]) != 8:
            parser.print_help()
            sys.exit(0)
        
        data = {'smtp_host' : args.smtp_host, 
                'smtp_user': args.smtp_user,
                'smtp_password': args.smtp_password,
                'to_email': args.to_email}
        unskript_ctl_config_create_notification('mail', data) 

    def delete_notification(self, type):
        """Implementing Delete of the cruD for Notification
        """
        if not type:
            return 
        
        if type.lower() == 'slack':
            unskript_ctl_config_delete_notification('slack')
        elif type.lower() == 'smtp':
            unskript_ctl_config_delete_notification('mail')
        else:
            print("ERROR: Wrong choice")
    
    def update_notification(self, type):
        """update_notification: Implementing cUrd for Notification
        """
        if not type:
            return 
        if type.lower() == 'slack':
            self.SLACK()
        elif type.lower() == 'smtp':
            self.SMTP()
        else:
            print("ERROR: Wrong choice")

    def read_notification(self, type):
        """read_notification: Implementing cuRd for Notification
        """
        if not type:
            return 
        retval = {}
        if type.lower() == 'slack':
            retval = unskript_ctl_config_read_notification('slack')
        elif type.lower() == 'smtp':
            retval = unskript_ctl_config_read_notification('mail')
        else:
            print("ERROR: Wrong choice")
        
        print(retval)

if __name__ == "__main__":
    """Notifcation class does the create of Crud"""
    Notification()