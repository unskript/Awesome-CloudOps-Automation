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


from pathlib import Path

#logging.basicConfig(
#    level=logging.DEBUG,
#    format='%(asctime)s [%(levelname)s] - %(message)s',
#    datefmt='%Y-%m-%d %H:%M:%S',
#    filename="/tmp/"
#)
UNSKRIPT_CTL_CONFIG_FILE="/unskript/etc/unskript_ctl_config.yaml"
UNSKRIPT_CTL_BINARY="/usr/local/bin/unskript-ctl.sh"

# Job config related
JOB_CONFIG_CHECKS_KEY_NAME = "checks"
JOB_CONFIG_SUITES_KEY_NAME = "suites"
JOB_CONFIG_CONNECTORS_KEY_NAME = "connector_types"
JOB_CONFIG_CUSTOM_SCRIPTS_KEY_NAME = "custom_scripts"
JOB_CONFIG_NOTIFY_KEY_NAME = "notify"

class Job():
    def __init__(
            self,
            checks: list[str],
            suites: list[str]=None,
            connectors: list[str] = None,
            custom_scripts: list[str] = None,
            notify: bool = False):
        self.checks = checks
        self.suites = suites
        self.connectors = connectors
        self.custom_scripts = custom_scripts
        self.notify = notify

    def parse(self):
        cmds = []
        notify = '--report' if self.notify == True else ''
        #TBD: Add support for suites and custom_scripts
        if self.checks is not None:
            cmds.append(f'{UNSKRIPT_CTL_BINARY} -rc --check {self.checks[0]} {notify}')
        if self.connectors is not None:
            # Need to construct the unskript-ctl command like
            # unskript-ctl.sh -rc --types aws,k8s
            connector_types_string = ','.join(self.connectors)
            cmds.append(f'{UNSKRIPT_CTL_BINARY} -rc --type {connector_types_string} {notify}')
        self.cmds = cmds
        print(self.cmds)


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

        if os.path.exists(self.config_file) == False:
            print(f"WARNING: {self.config_file} Not found!")
            return retval


        # We use EnvYAML to parse the hook file and give us the
        # dictionary representation of the YAML file
        retval = EnvYAML(self.config_file, strict=False)

        if not retval:
            print(f"WARNING: config file {self.config_file} content seems to be empty!")
            return retval

        self.parsed_config = retval

    def configure_credential(self):
        """configure_credential: This function is used to parse through the creds_dict and
        call the add_creds.sh method to populate the respective credential json
        """
        print('Processing credential section')
        creds_dict = self.parsed_config.get('credential')
        if creds_dict is None:
            print(f"ERROR: Nothing to configure credential with, found empty creds data")
            return

        for cred_type in creds_dict.keys():
            cred_list = creds_dict.get(cred_type)
            for cred in cred_list:
                if cred.get('enable') == False:
                    continue
                creds_cmd = ['/usr/local/bin/add_creds.sh', '-c', cred_type]
                for cred_key in cred:
                    # Skip name and enable keys
                    if cred_key in ['name', 'enable']:
                        continue
                    #TBD: Take care of arguments with no value
                    creds_cmd.extend(['--'+cred_key, cred.get(cred_key)])
                if creds_cmd:
                    print_cmd = ' '.join(creds_cmd)
                    print(f"Programming credential, command {print_cmd}")
                    self.run_command(creds_cmd)
                    print(f"Successfully programmed {cred_type}")
                else:
                    print(f"ERROR: No Credential {cred_type} was programmed")


    def configure_schedule(self):
        """configure_schedule: configures the schedule settings
        """
        print('Processing scheduler section')
        config = self.parsed_config.get('scheduler')
        if config is None:
            print(f"No scheduler configuration found")
            return

        cmds = []
        #unskript_crontab_file = "/unskript/etc/unskript_crontab.tab"
        unskript_crontab_file = "./unskript_crontab.tab"
        crons = []
        try:
            for schedule in config:
                if schedule.get('enable') == False:
                        continue
                cadence = schedule.get('cadence')
                script = schedule.get('script')
                # TBD: Validate cadence and script is valid
                crons.append(f'{cadence} {script}')
        except Exception as e:
            print(f'ERROR: Got error in programming cadence {cadence}, script {script}, {e}')
            raise e

        if crons:
            crons_per_line = "\n".join(crons)
            print(f'Schedule section: Programming crontab {crons_per_line}')
            try:
                with open(unskript_crontab_file, "w") as f:
                    f.write('\n'.join(crons))
                    f.write("\n")
                cmds = ['crontab', unskript_crontab_file]
                self.run_command(cmds)
            except Exception as e:
                print(f'Cron programming failed, {e}')
                raise e

    def parse_jobs(self):
        print('Processing jobs section')
        config = self.parsed_config.get('jobs')
        if config is None:
            print(f'No jobs config found')
            return

        for job in config:
            if job.get('enable') == False:
                continue
            job_name = job.get('name')
            if job_name is None:
                print("Skiping invalid job, name not found")
                continue
            # Check if the same job name exists
            if job_name in self.jobs:
                print(f'Skipping job name {job_name}, duplicate entry')
                continue
            checks = job.get(JOB_CONFIG_CHECKS_KEY_NAME)
            suites = job.get(JOB_CONFIG_SUITES_KEY_NAME)
            connectors = job.get(JOB_CONFIG_CONNECTORS_KEY_NAME)
            custom_scripts = job.get(JOB_CONFIG_CUSTOM_SCRIPTS_KEY_NAME)
            notify = job.get(JOB_CONFIG_NOTIFY_KEY_NAME, False)

            if checks is not None and len(checks) > 1:
                print(f'{job_name}: NOT SUPPORTED: more than 1 check')
                continue
            new_job = Job(checks, suites, connectors, custom_scripts, notify)
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
            print(f'{"".join(cmds)} failed, {e}')
            raise e

        return str(result.stdout)

def main():
    """main: This is the main function that gets called by the start.sh function
    to parse the unskript_ctl_config.yaml file and program credential and schedule as configured
    """
    config_parser = ConfigParser(UNSKRIPT_CTL_CONFIG_FILE)
    config_parser.parse_config_yaml()

    config_parser.configure_credential()
    config_parser.parse_jobs()
    config_parser.configure_schedule()

if __name__ == '__main__':
    main()
