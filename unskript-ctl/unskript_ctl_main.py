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
        if args.check_command == 'check':
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
                temp_list = self._db.cs.get_checks_by_connector(all_connectors, True)
                check_list = []
                for t in temp_list:
                    if t not in check_list:
                        check_list.append(t)
                status_of_run = self._check.run(checks_list=check_list)
            elif args.all is not False:
                check_list = self._db.cs.get_checks_by_connector("all", True)
                status_of_run = self._check.run(checks_list=check_list)
            else:
                parser.print_help()
                sys.exit(0) 
            self.uglobals['status_of_run'] = status_of_run
            self.update_audit_trail(collection_name='audit_trail', status_dict_list=status_of_run)
        
        if 'script' in args and args.command == 'run':
            self._script.run(script=args.script)

        
    def update_audit_trail(self, collection_name: str, status_dict_list: list):
        trail_data = {}
        id = ''
        k = str(datetime.now())
        p = f = e = 0
        id = self.uglobals.get('exec_id')
        if not id:
            id = uuid.uuid4() 

        trail_data[id] = {}
        trail_data[id]['time_stamp'] = k
        trail_data[id]['runbook'] = id + '_output.txt'
        trail_data[id]['check_status'] = {} 
        for sd in status_dict_list:
            if sd == {}:
                continue 
            for s in sd.get('result'):
                check_name, check_id, connector, status = s 
                if status == 'PASS':
                    p += 1
                elif status == 'FAIL':
                    f += 1
                elif status == 'ERROR':
                    e += 1
                trail_data[id]['check_status'][check_id] = {}
                trail_data[id]['check_status'][check_id]['check_name'] = check_name
                trail_data[id]['check_status'][check_id]['status'] = status
                trail_data[id]['check_status'][check_id]['connector'] = connector
                if self.uglobals.get('failed_result'):
                    c_name = connector + ':' + check_name
                    for name, obj in self.uglobals.get('failed_result').items():
                        if name in (c_name, check_name):
                            trail_data[id]['check_status'][check_id]['failed_objects'] = obj 
        
        trail_data[id]['summary'] = f'Summary (total/p/f/e): {p+e+f}/{p}/{f}/{e}'
        self._db.pss.update(collection_name=collection_name, data=trail_data)
        return id 

    def list_main(self, **kwargs):
        s = '\x1B[1;20;42m' + "~~~~ CLI Used ~~~~" + '\x1B[0m'
        print("")
        print(s)
        print("")
        print(f"\033[1m {sys.argv[0:]} \033[0m")
        print("")

        args = kwargs.get('args')
        if args.credential:
            self.list_credentials()
        elif args.sub_command == 'checks' and args.type:
            self.list_checks_by_connector(args)
        elif args.sub_command == 'checks' and args.all:
            self.list_checks_by_connector(args)
        elif args.command == 'list' and args.sub_command == 'failed-checks':
            self.display_failed_checks(args)
        
        
    def list_credentials(self):
        active_creds = []
        incomplete_creds = []
        for cred_file in self.creds_json_files:
            with open(cred_file, 'r') as f:
                c_data = json.load(f)

                c_type = c_data.get('metadata').get('type')
                c_name = c_data.get('metadata').get('name')
                if c_data.get('metadata').get('connectorData') != "{}":
                    active_creds.append((c_type, c_name))
                else:
                    incomplete_creds.append((c_type, c_name))
        combined = active_creds + incomplete_creds
        headers = ["#", "Connector Type", "Connector Name", "Status"]
        table_data = [headers]

        for index, (ctype, cname) in enumerate(combined, start=1):
            status = "Active" if index <= len(active_creds) else "Incomplete"
            table_data.append([index, ctype, cname, status])

        print(tabulate(table_data, headers='firstrow', tablefmt='fancy_grid'))

    def list_checks_by_connector(self, args):
        all_connectors = args.type 
        if not all_connectors:
            all_connectors = 'all'

        if not isinstance(all_connectors, list):
            all_connectors = [all_connectors]
        if len(all_connectors) == 1 and ',' in all_connectors[0]:
            all_connectors = all_connectors[0].split(',')
        for connector in all_connectors:
            connector = connector.replace(',', '')
        list_connector_table = [
            [TBL_HDR_LIST_CHKS_CONNECTOR, TBL_HDR_CHKS_NAME, TBL_HDR_CHKS_FN]]
        checks_list = self._db.cs.get_checks_by_connector(all_connectors, False)
        for cl in checks_list:
            list_connector_table.append(cl)
        print("")
        print(tabulate(list_connector_table, headers='firstrow', tablefmt='fancy_grid'))
        print("")
 

    def display_failed_checks(self, args):
        if args.all:
            connector = 'all'
        elif args.type:
            connector = args.type 
        else:
            connector = 'all'
        
        pss_content = self._db.pss.read(collection_name='audit_trail')
        failed_checks_table = [[TBL_HDR_DSPL_CHKS_NAME, TBL_HDR_FAILED_OBJECTS, TBL_HDR_DSPL_EXEC_ID]]
        for exec_id in pss_content.keys():
            execution_id = exec_id 
            for check_id in pss_content.get(exec_id).get('check_status').keys():
                if pss_content.get(exec_id).get('check_status').get(check_id).get('status').lower() == "fail":
                    if connector == 'all':
                        failed_checks_table += [[
                            pss_content.get(exec_id).get('check_status').get(check_id).get('check_name') + '\n' + f"(Test Failed on: {pss_content.get(exec_id).get('time_stamp')})",
                            pprint.pformat(pss_content.get(exec_id).get('check_status').get(check_id).get('failed_objects'), width=10),
                            execution_id
                        ]]
                    elif connector.lower() == pss_content.get(exec_id).get('check_status').get(check_id).get('connector').lower():
                        failed_checks_table += [[
                            pss_content.get(exec_id).get('check_status').get(check_id).get('check_name') + '\n' + f"(Test Failed on: {pss_content.get(exec_id).get('time_stamp')})",
                            pprint.pformat(pss_content.get(exec_id).get('check_status').get(check_id).get('failed_objects'), width=10),
                            execution_id
                        ]]

        print("")
        print(tabulate(failed_checks_table, headers='firstrow', tablefmt='fancy_grid'))
        print("")


    def show_main(self, **kwargs):
        s = '\x1B[1;20;42m' + "~~~~ CLI Used ~~~~" + '\x1B[0m'
        print("")
        print(s)
        print("")
        print(f"\033[1m {sys.argv[0:]} \033[0m")
        print("")
        if "args" in kwargs:
            args = kwargs.get('args')
        if "parser" in kwargs:
            parser = kwargs.get('parser')
        
        if args.show_command == 'audit-trail':
            pss_content = self._db.pss.read(collection_name='audit_trail')
            if args.all:
                self.print_all_result_table(pss_content=pss_content)
            elif args.type:
                self.print_connector_result_table(pss_content=pss_content, connector=args.type)
            elif args.execution_id:
                self.print_execution_result_table(pss_content=pss_content, execution_id=args.execution_id)                
            pass
        elif args.show_command == 'failed-logs':
            if args.execution_id:
                output = os.path.join(self.uglobals.get('UNSKRIPT_EXECUTION_DIR'), f'{args.execution_id}_output.txt')
                if os.path.exists(output) is False:
                    self.logger.error("Failed Log file does not exist. Please check the path!")
                    self._error(f"Unable to locate logs file for {args.execution_id}")
                    sys.exit(0)
                with open(output, 'r') as f:
                    output = json.loads(f.read())
                    print("\033[1mFAILED OBJECTS \033[0m \n")
                    for o in output:
                        if o.get('status') != 1:
                            print(f"\033[1m{o.get('name')} \033[0m")
                            p = yaml.safe_dump(o.get('objects'))
                            print(p)
                            print("\n")
            else:
                self.logger.error("Execution ID Is Empty, cannot find any logs")
                self._error(f"Execution ID {args.execution_id} Logs cannot be found!")
        else:
            parser.print_help()
        return 

    def print_all_result_table(self, pss_content: dict):
        if not pss_content:
            return 
        
        all_result_table = [["\033[1m Execution ID \033[0m",
                            "\033[1m Execution Summary \033[0m",
                            "\033[1m Execution Timestamp \033[0m"]]
        for item in pss_content.items():
            k, v = item
            summary_text = "\033[1m" + v.get('summary') + "\033[0m"
            check_names = "\033[1m" + str(k) + '\n' + "\033[0m"
            for k1, v1 in v.get('check_status').items():
                check_names += "    " + v1.get('check_name') + ' ['
                check_names += "\033[1m" + \
                    v1.get('status') + "\033[0m" + ']' + '\n'
            each_row = [[check_names, summary_text, v.get('time_stamp')]]
            all_result_table += each_row

        print(tabulate(all_result_table, headers='firstrow', tablefmt='fancy_grid'))


    def print_connector_result_table(self, pss_content: dict, connector: str):
        if not pss_content:
            return 
        
        connector_result_table = [["\033[1m Check Name \033[0m",
                                "\033[1m Run Status \033[0m",
                                "\033[1m Time Stamp \033[0m",
                                "\033[1m Execution ID \033[0m"]]
        
        for exec_id in pss_content.keys():
            execution_id = exec_id
            if pss_content.get(exec_id).get('check_status'):
                for check_id in pss_content.get(exec_id).get('check_status').keys():
                    if pss_content.get(exec_id).get('check_status').get(check_id).get('connector').lower() == connector.lower():
                        connector_result_table += [[pss_content.get(exec_id).get('check_status').get(check_id).get('check_name'),
                                                pss_content.get(exec_id).get('check_status').get(check_id).get('status'),
                                                pss_content.get(exec_id).get('time_stamp'),
                                                execution_id]]

        print(tabulate(connector_result_table,
                headers='firstrow', tablefmt='fancy_grid'))
        return 


    def print_execution_result_table(self, pss_content: dict, execution_id: str):
        execution_result_table = [["\033[1m Check Name \033[0m",
                                "\033[1m Failed Objects \033[0m",
                                "\033[1m Run Status \033[0m",
                                "\033[1m Time Stamp \033[0m"]]
        for exec_id in pss_content.keys():
            if exec_id == execution_id:
                ts = pss_content.get(exec_id).get('time_stamp')
                for check_ids in pss_content.get(exec_id).get('check_status').keys():
                    execution_result_table += [[pss_content.get(exec_id).get('check_status').get(check_ids).get('check_name'),
                                                pprint.pformat(pss_content.get(exec_id).get('check_status').get(check_ids).get('failed_objects'), 30),
                                                pss_content.get(exec_id).get('check_status').get(check_ids).get('status'),
                                                ts]]

        print(tabulate(execution_result_table,
                headers='firstrow', tablefmt='fancy_grid'))

    def service_main(self, **kwargs):
        raise NotImplementedError("NOT IMPLEMENTED")
    
    def debug_main(self, **kwargs):
        args = kwargs.get('args', None)
        parser = kwargs.get('parser', None)

        if args and args.command == 'debug':
            if args.start:
                self.start_debug(args.start)
                pass 
            elif args.stop:
                pass
            else: 
                self.logger.error("WRONG OPTION: Only start and stop are supported for debug")
                self._error("Wrong Option, only start and stop are supported")
        pass 

    def start_debug(self, args):
        """start_debug Starts Debug session. This function takes
        the remote configuration as input and if valid, starts
        the debug session.
        """
        if not args:
            print("ERROR: Insufficient information provided")
            return

        remote_config = args[0]
        remote_config = remote_config.replace('-','')

        if remote_config != "config":
            print(f"ERROR:The Allowed Parameter is --config, Given Flag is not recognized, --{remote_config}")
            return
        try:
            remote_config_file = args[1]
        except:
            print(f"ERROR: Not able to find the configuration to start debug session")
            return

        if os.path.exists(remote_config_file) is False:
            print(f"ERROR: Required Remote Configuration not present. Ensure {remote_config_file} file is present.")
            return

        openvpn_log_file = "/tmp/openvpn_client.log"
        command = [f"openvpn --config {remote_config_file} > {openvpn_log_file}"]
        try:
            process = subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
        except Exception as e:
            print(f"ERROR: Unable to run the command {command}, error {e}")
            return

        # Lets give few seconds for the subprocess to spawn
        try:
            outs, errs = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            # This is expected as the ovpn command needs to run indefinitely.
            pass
        except Exception as e:
            print(f'ERROR: Unable to communicate to child process, {e}')
            return

        # Lets verify if the openvpn process is really running
        running = False
        for proc in psutil.process_iter(['pid', 'name']):
            # Search for openvpn process.
            if proc.info['name'] == "openvpn":
                # Lets make sure we ensure Tunnel Interface is Created and Up!
                try:
                    intf_up_result = subprocess.run(["ip", "link", "show", "tun0"],
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE)
                    if intf_up_result.returncode == 0:
                        running = True
                    break
                except Exception as e:
                    print(f'ERROR: ip link show tun0 command failed, {e}')

        if running is True:
            print ("Successfully Started the Debug Session")
        else:
            self.logger.debug(f"Error Occured while starting the Debug Session. Here are the logs from openvpn")
            print(f"{bcolors.FAIL}Error Occured while starting the Debug Session. Here are the logs from openvpn{bcolors.ENDC}")
            print("===============================================================================================")
            with open(openvpn_log_file, "r") as fp:
                print(fp.read())
            # Bring down the ovpn process
            print("===============================================================================================")
            stop_debug()

    def stop_debug(self):
        """stop_debug Stops the Active Debug session.
        """
        for proc in psutil.process_iter(['pid', 'name']):
            # Search for openvpn process. On Docker, we dont expect
            # Multiple process of openvpn to run.
            if proc.info['name'] == "openvpn":
                process = psutil.Process(proc.info['pid'])
                process.terminate()
                process.wait()

        self.logger.debug("Stopped Active Debug session successfully")
        print("Stopped Active Debug session successfully")

    def notify(self, args):
        output_dir = create_execution_run_directory()
        summary_result = None
        failed_objects = None 
        output_json_file = None 
        mode = None
        if args.command == 'run' and args.check_command == 'check':
            summary_result = self.uglobals.get('status_of_run')
            failed_objects = self.uglobals.get('failed_result')
            mode = 'both'
        if args.script:
            output_json_file = os.path.join(output_dir,UNSKRIPT_SCRIPT_RUN_OUTPUT_FILE_NAME + '.json')
            mode = 'both'
        
        self._notification.notify(summary_results=summary_result,
                                  failed_objects=failed_objects,
                                  output_metadata_file=output_json_file,
                                  mode=mode)
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
    run_parser.add_argument('--script', type=str, help='Script name to run', required=False)
    check_subparser = run_parser.add_subparsers(dest='check_command')
    check_parser = check_subparser.add_parser('check', help='Run Check Option')
    check_parser.add_argument('--name', type=str, help='Check name to run')
    check_parser.add_argument('--type', type=str, help='Type of Check to run')
    check_parser.add_argument('--all', action='store_true', help='Run all checks')

    # List Option
    list_parser = subparsers.add_parser('list', help='List Options')
    list_parser.add_argument('--credential', action='store_true', help='List All credentials')
    list_check_subparser = list_parser.add_subparsers(dest='sub_command')
    list_check_parser  = list_check_subparser.add_parser('checks', help='List Check Options')
    list_check_parser.add_argument('--all', action='store_true', help='List All Checks')
    list_check_parser.add_argument('--type', 
                                   type=str, 
                                   help='List All Checks of given connector type',
                                   choices=CONNECTOR_LIST)
    list_failed_check_parser = list_check_subparser.add_parser('failed-checks', help='List Failed check options')
    list_failed_check_parser.add_argument('--all', action='store_true', help='Show All Failed Checks')
    list_failed_check_parser.add_argument('--type', 
                                   type=str, 
                                   help='List All Checks of given connector type',
                                   choices=CONNECTOR_LIST)
    # Show Option
    show_parser = subparsers.add_parser('show', help='Show Options')
    show_audit_subparser = show_parser.add_subparsers(dest='show_command')
    show_audit_parser = show_audit_subparser.add_parser('audit-trail', help='Show Audit Trail option')
    show_audit_parser.add_argument('--all',
                                   action='store_true',
                                   help='List trail of all checks across all connectors')
    show_audit_parser.add_argument('--type',
                                   type=str,
                                   choices=CONNECTOR_LIST,
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
    debug_parser.add_argument('--start',
                                      help='Start debug session. Example [--start --config /tmp/config.ovpn]',
                                      type=str,
                                      nargs=REMAINDER)
    debug_parser.add_argument('--stop',
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
    

    # Lets re-arrange arguments such that parse_args is efficient with
    # the rules defined above
    def rearrange_argv(argv):
        script_idx = argv.index('--script') if '--script' in argv else -1
        check_idx = argv.index('check') if 'check' in argv else -1
        report_idx = argv.index('--report') if '--report' in argv else -1
        run_idx = argv.index('run') if 'run' in argv else -1
        
        if script_idx != -1 and check_idx != -1:
            if script_idx > check_idx:
                argv.remove('--script')
                script_name = argv.pop(script_idx)
                argv.insert(run_idx + 1, '--script')
                argv.insert(run_idx + 2, script_name)
        
        if report_idx != -1 and check_idx != -1:
            if report_idx > check_idx:
                argv.remove('--report')
                argv.insert(run_idx, '--report')

        return argv
    
    argv = sys.argv[1:].copy()
    argv = rearrange_argv(argv)
    args = parser.parse_args(argv)

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

    if args.command == 'run' and  args.report:
        uc.notify(args)

if __name__ == '__main__':
    main()