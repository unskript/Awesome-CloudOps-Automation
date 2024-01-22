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
import logging
import subprocess
import os
import sys
from envyaml import EnvYAML
from unskript_utils import bcolors, UNSKRIPT_EXECUTION_DIR

#logging.basicConfig(
#    level=logging.DEBUG,
#    format='%(asctime)s [%(levelname)s] - %(message)s',
#    datefmt='%Y-%m-%d %H:%M:%S',
#    filename="/tmp/"
#)
UNSKRIPT_CTL_CONFIG_FILE="/etc/unskript/unskript_ctl_config.yaml"
UNSKRIPT_CTL_BINARY="/usr/local/bin/unskript-ctl.sh"


# Job config related
JOB_CONFIG_CHECKS_KEY_NAME = "checks"
JOB_CONFIG_INFO_KEY_NAME = "info"
JOB_CONFIG_SUITES_KEY_NAME = "suites"
JOB_CONFIG_CONNECTORS_KEY_NAME = "connector_types"
JOB_CONFIG_CUSTOM_SCRIPTS_KEY_NAME = "custom_scripts"
JOB_CONFIG_NOTIFY_KEY_NAME = "notify"

# Credential section related
CREDENTIAL_CONFIG_SKIP_VALUE_FOR_ARGUMENTS = ["no-verify-certs", "no-verify-ssl", "use-ssl"]

# Global section related
GLOBAL_CONFIG_AUDIT_PERIOD_KEY_NAME = "audit_period"
GLOBAL_DEFAULT_AUDIT_PERIOD = 90

# Checks section related
CHECKS_ARGUMENTS_KEY_NAME = "arguments"
CHECKS_GLOBAL_KEY_NAME = "global"
CHECKS_MATRIX_KEY_NAME = "matrix"

# Config top level keys
CONFIG_GLOBAL = "global"
CONFIG_CHECKS = "checks"
CONFIG_CREDENTIAL = "credential"
CONFIG_NOTIFICATION = "notification"
CONFIG_JOBS = "jobs"
CONFIG_SCHEDULER = "scheduler"
CONFIG_REMOTE_DEBUGGING = "remote_debugging"

class Job():
    def __init__(
            self,
            job_name: str,
            checks: list[str],
            info: list[str],
            suites: list[str]=None,
            connectors: list[str] = None,
            custom_scripts: list[str] = None,
            notify: bool = False):
        self.job_name = job_name
        self.checks = checks
        self.info = info
        self.suites = suites
        self.connectors = connectors
        self.custom_scripts = custom_scripts
        self.notify = notify
    

    def parse(self):
        cmds = []
        notify = '--report' if self.notify is True else ''
        # Today, we dont support
        # check --name <> check --type k8s --script
        # So, if both check names and types are configured, we will split it
        # into 2 commands.
        # We will combine script with --types and make the --name as separate
        # command.

        combine_check_types_and_script = False
        combine_check_names_and_script = False
        if self.checks is not None and len(self.checks) != 0 and self.custom_scripts is not None and len(self.custom_scripts) != 0:
            combine_check_names_and_script = True
        if self.connectors is not None and len(self.connectors) != 0 and self.custom_scripts is not None and len(self.custom_scripts) != 0:
            combine_check_names_and_script = False
            combine_check_types_and_script = True

        # full_command will contain the full command if both check and --script
        # are specified.
        full_command = None
        if self.checks is not None and len(self.checks) != 0:
            if combine_check_names_and_script:
                full_command = f'{UNSKRIPT_CTL_BINARY} run check --name {self.checks[0]}'
            else:
                cmds.append(f'{UNSKRIPT_CTL_BINARY} run check --name {self.checks[0]} {notify}')
            print(f'Job: {self.job_name} contains check: {self.checks[0]}')


        if self.connectors is not None and len(self.connectors) != 0:
            # Need to construct the unskript-ctl command like
            # unskript-ctl.sh run check --types aws,k8s
            connector_types_string = ','.join(self.connectors)
            print(f'Job: {self.job_name} contains connector types: {connector_types_string}')
            if combine_check_types_and_script:
                full_command = f'{UNSKRIPT_CTL_BINARY} run check --type {connector_types_string}'
            else:
                cmds.append(f'{UNSKRIPT_CTL_BINARY} run check --type {connector_types_string} {notify}')
        

        accessmode = os.F_OK | os.X_OK
        if self.custom_scripts is not None and len(self.custom_scripts) != 0:
            # Do basic checks, like the binary exists, permission is fine.
            filtered_scripts = []
            filtered_scripts = self.custom_scripts
            #for script in self.custom_scripts:
            #    command = script.split(' ')
            #    if not os.path.exists(command[0]):
            #        print(f'''{bcolors.FAIL}{command[0]} does not exist. Please ensure that you
            #             provide the full path. {bcolors.ENDC}
            #            ''')
            #        continue
            #    if not os.access(command, accessmode):
            #        print(f'{bcolors.FAIL}{command} is not executable. {bcolors.ENDC}')
            #        continue
            #    filtered_scripts.append(script)
            if filtered_scripts:
                combined_script = ';'.join(filtered_scripts)
                print(f'Job: {self.job_name} contains custom script: {combined_script}')
                if combine_check_types_and_script or combine_check_names_and_script:
                    full_command += f' --script "{combined_script}" {notify}'
                else:
                    cmds.append(f'{UNSKRIPT_CTL_BINARY} run --script "{combined_script}" {notify}')

        if full_command is not None:
            cmds.append(full_command)
        
        # For info gathering
        if self.info:
            cmds.append('--info')

        self.cmds = cmds

class ConfigParser():
    def __init__(self, config_file: str):
        self.config_file = config_file
        # Dictionary of jobs, with job name being the key.
        self.jobs = {}
        self.tunnel_up_cmd = None
        self.tunnel_down_cmd = None
        self.upload_logs_files_cmd = None

    def parse_config_yaml(self) -> dict:
        """parse_config_yaml: This function parses the config yaml file and converts the
        content as a python dictionary and returns back to the caller.
        """
        retval = {}

        if os.path.exists(self.config_file) is False:
            print(f"{bcolors.FAIL} {self.config_file} Not found!{bcolors.ENDC}")
            sys.exit(0)

        # We use EnvYAML to parse the hook file and give us the
        # dictionary representation of the YAML file
        try:
            retval = EnvYAML(self.config_file, strict=False)
            if not retval:
                print(f"{bcolors.WARNING} Parsing config file {self.config_file} failed{bcolors.ENDC}")
                sys.exit(0)
        except Exception as e:
            print(f"{bcolors.FAIL} Parsing config file {self.config_file} failed{bcolors.ENDC}")
            sys.exit(0)

        self.parsed_config = retval

    def parse_global(self):
        """parse_global: This function parses the global section of the config.
        """
        print('###################################')
        print(f'{bcolors.HEADER}Processing global section{bcolors.ENDC}')
        print('###################################')
        config = self.parsed_config.get(CONFIG_GLOBAL)
        if config is None:
            print(f"{bcolors.WARNING}Global: Nothing to configure credential with, found empty creds data{bcolors.ENDC}")
            return

        # Process the audit_period config
        audit_period = config.get(GLOBAL_CONFIG_AUDIT_PERIOD_KEY_NAME, GLOBAL_DEFAULT_AUDIT_PERIOD)
        print(f'Global: audit period {audit_period} days')
        self.audit_period = audit_period

    def parse_checks(self):
        """parse_checks: This function parses the checks section of the config.
        """
        print('###################################')
        print(f'{bcolors.HEADER}Processing checks section{bcolors.ENDC}')
        print('###################################')
        config = self.parsed_config.get(CONFIG_CHECKS)
        if config is None:
            print(f"{bcolors.WARNING}Checks: No checks config{bcolors.ENDC}")
            return
        arguments = config.get(CHECKS_ARGUMENTS_KEY_NAME)
        if arguments is None:
            print(f"{bcolors.WARNING}Checks: No arguments config{bcolors.ENDC}")
            return
        global_args = arguments.get(CHECKS_GLOBAL_KEY_NAME)
        if global_args is None:
            print(f"{bcolors.WARNING}Checks: No global config{bcolors.ENDC}")
            return
        # Ensure we atmost have ONLY one matrix argument
        matrix_args = global_args.get(CHECKS_MATRIX_KEY_NAME)
        if matrix_args is None:
            return
        if len(matrix_args) > 1:
            print(f'{bcolors.FAIL} Only one matrix argument supported {bcolors.ENDC}')
            return

    def configure_credential(self):
        """configure_credential: This function is used to parse through the creds_dict and
        call the add_creds.sh method to populate the respective credential json
        """
        print('###################################')
        print(f'{bcolors.HEADER}Processing credential section{bcolors.ENDC}')
        print('###################################')
        creds_dict = self.parsed_config.get(CONFIG_CREDENTIAL)
        if creds_dict is None:
            print(f"{bcolors.WARNING}Credential: Nothing to configure credential with, found empty creds data{bcolors.ENDC}")
            return

        for cred_type in creds_dict.keys():
            cred_list = creds_dict.get(cred_type)
            for cred in cred_list:
                name = cred.get('name')
                if cred.get('enable') is False:
                    print(f'Credential: Skipping type {cred_type}, name {name}')
                    continue
                creds_cmd = ['/usr/local/bin/add_creds.sh', '-c', cred_type]
                try:
                    print(f'Credential: Programming type {cred_type}, name {name}')
                    for cred_key in cred:
                        # Skip name and enable keys
                        if cred_key in ['name', 'enable']:
                            continue
                        # Certain arguments dont need extra value part like -no-verify-certs
                        if cred_key in CREDENTIAL_CONFIG_SKIP_VALUE_FOR_ARGUMENTS:
                            creds_cmd.extend(['--'+cred_key])
                        else:
                            creds_cmd.extend(['--'+cred_key, str(cred.get(cred_key))])
                    if creds_cmd:
                        #print_cmd = ' '.join(creds_cmd)
                        self.run_command(creds_cmd)
                        print(f"{bcolors.OKGREEN}Credential: Successfully programmed {cred_type}, name {name}{bcolors.ENDC}")
                except Exception as e:
                    print(f'{bcolors.FAIL}Credential: Failed to program {cred_type}, name {name}{bcolors.ENDC}')
                    continue



    def configure_schedule(self):
        """configure_schedule: configures the schedule settings
        """
        print('###################################')
        print(f'{bcolors.HEADER}Processing scheduler section{bcolors.ENDC}')
        print('###################################')
        config = self.parsed_config.get(CONFIG_SCHEDULER)
        if config is None:
            print(f"{bcolors.WARNING}Scheduler: No scheduler configuration found{bcolors.ENDC}")
            return

        unskript_crontab_file = "/etc/unskript/unskript_crontab.tab"
        crons = []
        try:
            for schedule in config:
                if schedule.get('enable') is False:
                    print(f'Skipping')
                    continue
                cadence = schedule.get('cadence')
                job_name = schedule.get('job_name')
                # look up the job name and get the commands
                job = self.jobs.get(job_name)
                if job is None:
                    print(f'{bcolors.FAIL}Schedule: Unknown job name {job_name}. Please check the jobs section and ensure the job is defined{bcolors.ENDC}')
                    continue
                print(f'Schedule: cadence {cadence}, job name: {job_name}')
                if len(job.cmds) == 0:
                    print(f'{bcolors.WARNING}Scheduler: Empty job {job.job_name}, not adding to schedule{bcolors.ENDC}')
                    continue
                script = '; '.join(job.cmds)
                # TBD: Validate cadence and script is valid
                crons.append(f'{cadence} {script}')
        except Exception as e:
            print(f'{bcolors.FAIL}Schedule: Got error in programming cadence {cadence}, script {script}, {e}{bcolors.ENDC}')
            #raise e
            return

        try:
            with open(unskript_crontab_file, "w") as f:
                # Since crontabs dont inherit the environmnent variables, we have to
                # do it explicitly.
                for name, value in os.environ.items():
                    if value != "":
                        f.write(f'{name}={value}')
                        f.write("\n")
                if crons:
                    cmds = []
                    crons_per_line = "\n".join(crons)
                    print(f'Schedule: Programming crontab {crons_per_line}')
                    f.write('\n'.join(crons))
                    f.write("\n")
                # Add the audit period cron job as well, to be run daily.
                audit_cadence = "0 0 * * *"
                # delete_old_files_command = f'/usr/bin/find {UNSKRIPT_EXECUTION_DIR} -type f -mtime +{self.audit_period} -exec rm -f {{}} \;'
                delete_old_files_command = f'/opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py'
                print(f'{bcolors.OKGREEN}Adding audit log deletion cron job entry, {audit_cadence} {delete_old_files_command}{bcolors.ENDC}')
                f.write(f'{audit_cadence} {delete_old_files_command}')
                f.write("\n")

                # If there is remote_debugging commands, add them too
                if self.tunnel_up_cmd:
                    f.write(self.tunnel_up_cmd)
                    f.write("\n")
                if self.tunnel_down_cmd:
                    f.write(self.tunnel_down_cmd)
                    f.write("\n")
                if self.upload_logs_files_cmd:
                    f.write(self.upload_logs_files_cmd)
                    f.write("\n")

            cmds = ['crontab', unskript_crontab_file]
            self.run_command(cmds)
        except Exception as e:
            print(f'{bcolors.FAIL}Schedule: Cron programming failed, {e}{bcolors.ENDC}')
            #raise e

    def parse_jobs(self):
        print('###################################')
        print(f'{bcolors.HEADER}Processing jobs section{bcolors.ENDC}')
        print('###################################')
        config = self.parsed_config.get(CONFIG_JOBS)
        if config is None:
            print(f'{bcolors.WARNING}Jobs: No jobs config found{bcolors.ENDC}')
            return

        for job in config:
            job_name = job.get('name')
            if job_name is None:
                print(f"{bcolors.OKBLUE}Jobs: Skipping invalid job, name not found{bcolors.ENDC}")
                continue
            if job.get('enable') is False:
                print(f'Jobs: Skipping {job_name}')
                continue
            # Check if the same job name exists
            if job_name in self.jobs:
                print(f'{bcolors.WARNING}Jobs: Skipping job name {job_name}, duplicate entry{bcolors.ENDC}')
                continue
            checks = job.get(JOB_CONFIG_CHECKS_KEY_NAME)
            info = job.get(JOB_CONFIG_INFO_KEY_NAME)
            suites = job.get(JOB_CONFIG_SUITES_KEY_NAME)
            connectors = job.get(JOB_CONFIG_CONNECTORS_KEY_NAME)
            custom_scripts = job.get(JOB_CONFIG_CUSTOM_SCRIPTS_KEY_NAME)
            notify = job.get(JOB_CONFIG_NOTIFY_KEY_NAME, False)
            if checks is not None and len(checks) > 1:
                print(f'{job_name}: NOT SUPPORTED: more than 1 check')
                continue
            new_job = Job(job_name, checks, info, suites, connectors, custom_scripts, notify)
            new_job.parse()
            self.jobs[job_name] = new_job

    def run_command(self, cmds:list)->str:
        """run_command: Runs the command in a subprocess and returns the output
        or raise excetption
        """
        try:
            result = subprocess.run(cmds,
                                    capture_output=True,
                                    check=True)
        except Exception as e:
            print(f'cmd: {" ".join(cmds)} failed, {e}')
            raise e

        return str(result.stdout)

    def parse_remote_debugging(self):
        print('###################################')
        print(f'{bcolors.HEADER}Processing remote debugging section{bcolors.ENDC}')
        print('###################################')
        config = self.parsed_config.get(CONFIG_REMOTE_DEBUGGING)
        if config is None:
            print(f'{bcolors.WARNING}Remote_debugging: No remote_debugging config found{bcolors.ENDC}')
            return
        if config.get('enable') is False:
            print(f'{bcolors.WARNING} Skipping remote_debugging section{bcolors.ENDC}')
            return
        upload_log_files_cadence = config.get('upload_log_files_cadence', None)
        if upload_log_files_cadence is not None:
            print(f'{bcolors.HEADER} Programming upload_log_files_cadence {upload_log_files_cadence}')
            self.upload_logs_files_cmd = f'{upload_log_files_cadence} /opt/unskript/bin/python /usr/local/bin/unskript_ctl_upload_session_logs.py'
        ovpn_file = config.get('ovpn_file', None)
        if ovpn_file is None:
            print(f'{bcolors.FAIL}Please mention the ovpn file location{bcolors.ENDC}')
            return
        tunnel_up_cadence = config.get('tunnel_up_cadence', None)
        tunnel_down_cadence = config.get('tunnel_down_cadence', None)
        # Check both of them are present.
        if (tunnel_up_cadence is None and tunnel_down_cadence is not None) or (tunnel_up_cadence is not None and tunnel_down_cadence is None):
            print(f'{bcolors.FAIL} Please ensure both tunnel_up_cadence and tunnel_down_cadence is configured{bcolors.ENDC}')
            return
        if tunnel_up_cadence is not None:
            print(f'{bcolors.HEADER} Programming tunnel_up_cadence {tunnel_up_cadence}')
            self.tunnel_up_cmd = f'{tunnel_up_cadence} /usr/local/bin/unskript-ctl.sh debug --start  {ovpn_file}'
        if tunnel_down_cadence is not None:
            print(f'{bcolors.HEADER} Programming tunnel_down_cadence {tunnel_down_cadence}')
            self.tunnel_down_cmd = f'{tunnel_down_cadence} /usr/local/bin/unskript-ctl.sh debug --stop'

def main():
    """main: This is the main function that gets called by the start.sh function
    to parse the unskript_ctl_config.yaml file and program credential and schedule as configured
    """
    config_parser = ConfigParser(UNSKRIPT_CTL_CONFIG_FILE)
    config_parser.parse_config_yaml()

    config_parser.parse_global()
    config_parser.parse_checks()
    config_parser.configure_credential()
    config_parser.parse_jobs()
    config_parser.parse_remote_debugging()
    config_parser.configure_schedule()

if __name__ == '__main__':
    main()
