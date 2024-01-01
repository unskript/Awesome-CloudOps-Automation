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

from datetime import datetime 
from argparse import ArgumentParser, REMAINDER, SUPPRESS
from unskript_ctl_debug import *
from unskript_ctl_database import *
from unskript_ctl_run import *
from unskript_ctl_list import * 
from unskript_ctl_notification import * 
from unskript_utils import * 
from unskript_factory import *
from unskript_ctl_version import * 

class UnskriptCtl(UnskriptFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger.info("Initializing UnskriptCtl")
        self.logger.info(f"\tVERSION: {VERSION}")
        self.logger.info(f"\tAUTHORS: {AUTHOR}")
        self.logger.info(f"\tBUILD_NUMBER: {BUILD_NUMBER}")
        self._config = ConfigParserFactory()
        self._notification = Notification()
        self._check = Checks()
        self._script = Script()
        self._db = DBInterface() 
    
    def create_creds(self, **kwargs):
        if 'connector_type' not in kwargs:
            self.logger.error(f"connector_type is a mandatory argument to be pased for create_creds")
            self._error("Please pass connector_type is a mandatory argument")
            sys.exit(0)
        if 'connector_data_file' not in kwargs:
            self.logger.error(f"connector_data_file is a mandatory argument to be pased for create_creds")
            self._error("Please pass connector_data_file is a mandatory argument")
            sys.exit(0)
        connector_type = kwargs.get('connector_type')
        connector_data_file = kwargs.get('connector_data_file')
        if connector_type in ("k8s", "kubernetes"):
            with open(connector_data_file, 'r', encoding='utf-8') as f:
                creds_data = f.read()
            k8s_creds_file = os.path.join(os.environ.get('HOME'),  CREDENTIAL_DIR + '/k8screds.json')
            with open(k8s_creds_file, 'r', encoding='utf-8') as f:
                k8s_creds_content = json.loads(f.read())
            try:
                k8s_creds_content['metadata']['connectorData'] = json.dumps({"kubeconfig": creds_data})
                with open(k8s_creds_file, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(k8s_creds_content, indent=2))
            except:
                self.logger.error("Not able to write k8s creds data to k8screds.json, check permission")
                self._error("Not able to write k8s creds data to k8screds.json")
                sys.exit(1)
            finally:
                print("Successfully Created K8S Credential")
        else:
            self.display_creds_ui()
    
    def display_creds_ui(self):
        try:
            from creds_ui import main as ui
            ui()
        except:
            self.logger.error("Required python library creds_ui is not packaged")
            self._error("Required python library creds_ui is not packaged")
    
    def save_check_names(self, **kwargs):
        if 'filename' in kwargs:
            filename = kwargs.get('filename')
        else:
            filename = '/tmp/checknames.txt'
        list_of_names = self._db.cs.get_all_check_names()
        with open(filename, 'w', encoding='utf-8') as f:
            for name in list_of_names:
                f.write(name + '\n')
        self.logger.info(f"Saved  {len(list_of_names)} Check Names!")
    
    def run_main(self, **kwargs):
        args = parser = None 
        if 'args' in kwargs:
            args = kwargs.get('args')
        if 'parser' in kwargs:
            parser = kwargs.get('parser')
        
        if not args or not parser:
            self.logger.error("ARGS and/or Parser sent to run_main is None!")
            self._error("ARGS and/or Parser sent to run_main is None")
            sys.exit(0)
        status_of_run = []
        if args.name is not None:
            checks_list = self._db.cs.get_check_by_name(check_name=str(args.name))
            status_of_run = self._check.run(checks_list=checks_list)
        elif args.type is not None:
            all_connectors = args.type 
            if not isinstance(all_connectors, list):
                all_connectors = [all_connectors]
            if len(all_connectors) == 1 and ',' in all_connectors[0]:
                all_connectors = all_connectors[0].split(',')
            for connector in all_connectors:
                connector = connector.replace(',', '')
            temp_list = self._db.cs.get_checks_by_connector(connector_names=all_connectors)
            check_list = []
            for t in temp_list:
                if t not in check_list:
                    check_list.append(t)
            check_list = self._db.cs.get_checks_by_connector(connector_names=all_connectors)
            status_of_run = self._check.run(checks_list=check_list)
        elif args.all is not False:
            check_list = self._db.cs.get_checks_by_connector(connector_names="all", full_snippet=True)
            status_of_run = self._check.run(checks_list=check_list)
        else:
            parser.print_help()
            sys.exit(0) 
        self._db.pss.update(collection_name='audit_trail', data=status_of_run)

    def list_main(self, **kwargs):
        pass 

    def show_main(self, **kwargs):
        pass 

    def service_main(self, **kwargs):
        pass

    pass 

def main():
    uc = UnskriptCtl()
    parser = ArgumentParser(prog='unskript-ctl')
    description = ""
    description = description + str("\n")
    description = description + str("\t  Welcome to unSkript CLI Interface \n")
    description = description + str(f"\t\t   VERSION: {VERSION} \n")
    description = description + str(f"\t\t   BUILD_NUMBER: {BUILD_NUMBER} \n")
    parser.description = description

    subparsers = parser.add_subparsers(dest='command', help='Available Commands')
    # Run Option
    run_parser = subparsers.add_parser('run', help='Run Options')
    check_subparser = run_parser.add_subparsers()
    check_parser = check_subparser.add_parser('check', help='Run Check Option')
    check_parser.add_argument('--name', type=str, help='Check name to run')
    check_parser.add_argument('--type', type=str, help='Type of Check to run')
    check_parser.add_argument('--all', action='store_true', help='Run all checks')
    run_parser.add_argument('--script', type=str, help='Script name to run', required=False)

    # List Option
    list_parser = subparsers.add_parser('list', help='List Options')
    list_parser.add_argument('--failed-checks', type=str, help='List Failed Checks')
    list_check_subparser = list_parser.add_subparsers()
    list_check_parser  = list_check_subparser.add_parser('check', help='List Check Options')
    list_check_parser.add_argument('--all', action='store_true', help='List All Checks')
    list_check_parser.add_argument('--type', 
                                   type=str, 
                                   help='List All Checks of given connector type',
                                   choices=CONNECTOR_LIST)

    # Show Option
    show_parser = subparsers.add_parser('show', help='Show Options')
    show_audit_subparser = show_parser.add_subparsers()
    show_audit_parser = show_audit_subparser.add_parser('audit-trail', help='Show Audit Trail option')
    show_audit_parser.add_argument('--all',
                                   action='store_true',
                                   help='List trail of all checks across all connectors')
    show_audit_parser.add_argument('--type',
                                   dest='connector_type',
                                   type=str,
                                   help='Show Audit trail for checks for given connector')
    show_audit_parser.add_argument('--execution_id',
                                   type=str,
                                   help='Execution ID for which the audit trail should be shown')
    
    show_flogs_parser = show_audit_subparser.add_parser('failed-logs', help='Show Failed Logs option')
    show_flogs_parser.add_argument('--execution_id',
                                   type=str,
                                   help='Execution ID for which the logs should be fetched')
    
    # Debug / Service Option
    debug_parser = subparsers.add_parser('debug', help='Debug Option')
    debug_subparser = debug_parser.add_subparsers()
    debug_service_parser = debug_subparser.add_parser('debug-session', help='Show Debug Session Option')
    debug_service_parser.add_argument('--start',
                                      help='Start debug session. Example [--start --config /tmp/config.ovpn]',
                                      type=str,
                                      nargs=REMAINDER)
    debug_service_parser.add_argument('--stop',
                                      help='Stop debug session',
                                      action='store_true') 

    # Create Credential
    parser.add_argument('--create-credential',
                        type=str,
                        nargs=REMAINDER,
                        help='Create Credential [-creds-type creds_file_path]')
    # Save Check Names
    parser.add_argument('--save-check-names',
                        type=str,
                        help=SUPPRESS)
    

    # Report Option
    parser.add_argument('--report',
                        action='store_true',
                        help='Report Results')

    
    args = parser.parse_args()

    if len(sys.argv) <= 2:
        parser.print_help()
        sys.exit(0)
    
    if args.command == 'run':
        uc.run_main(args=args, parser=parser)
    elif args.command == 'list':
        uc.list_main(args=args, parser=parser)
    elif args.command == 'show':
        uc.show_main(args=args, parser=parser)
    elif args.command == 'debug':
        uc.service_main(args=args, parser=parser)
    elif args.create_credential not in ('', None):
        if len(args.create_credential) == 0:
            uc.display_creds_ui()
        else:
            uc.create_creds(args.create_credential)
    elif args.save_check_names not in ('', None):
        uc.save_check_names(args.save_check_names)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()