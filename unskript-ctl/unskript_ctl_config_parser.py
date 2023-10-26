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
from envyaml import EnvYAML
import sys


from pathlib import Path

#logging.basicConfig(
#    level=logging.DEBUG,
#    format='%(asctime)s [%(levelname)s] - %(message)s',
#    datefmt='%Y-%m-%d %H:%M:%S',
#    filename="/tmp/"
#)
UNSKRIPT_CTL_CONFIG_FILE="/etc/unskript/unskript_ctl_config.yaml"
UNSKRIPT_CTL_BINARY="/usr/local/bin/unskript-ctl.sh"
UNSKRIPT_EXECUTION_DIR="/unskript/data/execution/workspace/"

# Job config related
JOB_CONFIG_CHECKS_KEY_NAME = "checks"
JOB_CONFIG_SUITES_KEY_NAME = "suites"
JOB_CONFIG_CONNECTORS_KEY_NAME = "connector_types"
JOB_CONFIG_CUSTOM_SCRIPTS_KEY_NAME = "custom_scripts"
JOB_CONFIG_NOTIFY_KEY_NAME = "notify"

# Credential section related
CREDENTIAL_CONFIG_SKIP_VALUE_FOR_ARGUMENTS = ["no-verify-certs", "no-verify-ssl", "use-ssl"]

# Global section related
GLOBAL_CONFIG_AUDIT_PERIOD_KEY_NAME = "audit_period"
GLOBAL_DEFAULT_AUDIT_PERIOD = 90

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Job():
    def __init__(
            self,
            job_name: str,
            checks: list[str],
            suites: list[str]=None,
            connectors: list[str] = None,
            custom_scripts: list[str] = None,
            notify: bool = False):
        self.job_name = job_name
        self.checks = checks
        self.suites = suites
        self.connectors = connectors
        self.custom_scripts = custom_scripts
        self.notify = notify

    def parse(self):
        cmds = []
        notify = '--report' if self.notify is True else ''
        #TBD: Add support for suites and custom_scripts
        if self.checks is not None and len(self.checks) != 0:
            cmds.append(f'{UNSKRIPT_CTL_BINARY} -rc --check {self.checks[0]} {notify}')
            print(f'Job: {self.job_name} contains check: {self.checks[0]}')
        if self.connectors is not None and len(self.connectors) != 0:
            # Need to construct the unskript-ctl command like
            # unskript-ctl.sh -rc --types aws,k8s
            connector_types_string = ','.join(self.connectors)
            print(f'Job: {self.job_name} contains connector types: {connector_types_string}')
            cmds.append(f'{UNSKRIPT_CTL_BINARY} -rc --type {connector_types_string} {notify}')
        self.cmds = cmds

class ConfigParser():
    def __init__(self, config_file: str):
        self.config_file = config_file
        # Dictionary of jobs, with job name being the key.
        self.jobs = {}

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
        config = self.parsed_config.get('global')
        if config is None:
            print(f"{bcolors.WARNING}Global: Nothing to configure credential with, found empty creds data{bcolors.ENDC}")
            return

        # Process the audit_period config
        audit_period = config.get(GLOBAL_CONFIG_AUDIT_PERIOD_KEY_NAME, GLOBAL_DEFAULT_AUDIT_PERIOD)
        print(f'Global: audit period {audit_period} days')
        self.audit_period = audit_period


    def configure_credential(self):
        """configure_credential: This function is used to parse through the creds_dict and
        call the add_creds.sh method to populate the respective credential json
        """
        print('###################################')
        print(f'{bcolors.HEADER}Processing credential section{bcolors.ENDC}')
        print('###################################')
        creds_dict = self.parsed_config.get('credential')
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
                        print_cmd = ' '.join(creds_cmd)
                        self.run_command(creds_cmd)
                        print(f"{bcolors.OKGREEN}Credential: Successfully programmed {cred_type}, name {name}, cmd {print_cmd}{bcolors.ENDC}")
                except Exception as e:
                    print(f'{bcolors.FAIL}Credential: Failed to program {cred_type}, name {name}{bcolors.ENDC}')
                    continue



    def configure_schedule(self):
        """configure_schedule: configures the schedule settings
        """
        print('###################################')
        print(f'{bcolors.HEADER}Processing scheduler section{bcolors.ENDC}')
        print('###################################')
        config = self.parsed_config.get('scheduler')
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
                delete_old_files_command = f'/usr/bin/find {UNSKRIPT_EXECUTION_DIR} -name "*.ipynb" -type f -mtime +{self.audit_period} -exec rm -f {{}} \;'
                print(f'{bcolors.OKGREEN}Adding audit log deletion cron job entry, {audit_cadence} {delete_old_files_command}{bcolors.ENDC}')
                f.write(f'{audit_cadence} {delete_old_files_command}')
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
        config = self.parsed_config.get('jobs')
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
            suites = job.get(JOB_CONFIG_SUITES_KEY_NAME)
            connectors = job.get(JOB_CONFIG_CONNECTORS_KEY_NAME)
            custom_scripts = job.get(JOB_CONFIG_CUSTOM_SCRIPTS_KEY_NAME)
            notify = job.get(JOB_CONFIG_NOTIFY_KEY_NAME, False)

            if checks is not None and len(checks) > 1:
                print(f'{job_name}: NOT SUPPORTED: more than 1 check')
                continue
            new_job = Job(job_name, checks, suites, connectors, custom_scripts, notify)
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

def main():
    """main: This is the main function that gets called by the start.sh function
    to parse the unskript_ctl_config.yaml file and program credential and schedule as configured
    """
    config_parser = ConfigParser(UNSKRIPT_CTL_CONFIG_FILE)
    config_parser.parse_config_yaml()

    config_parser.parse_global()
    config_parser.configure_credential()
    config_parser.parse_jobs()
    config_parser.configure_schedule()

if __name__ == '__main__':
    main()
