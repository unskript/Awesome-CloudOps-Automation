#!/usr/bin/env python
#
# Copyright (c) 2024 unSkript.com
# All rights reserved.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE
#
#

import argparse
import json
import os
import sys
import yaml
from diagnostics_worker import *


class DiagnosticsScript:
    def __init__(self, args):
        self.args = args
        self.calling_map = {
            "k8s": "k8s_diagnostics",
            "mongodb": "mongodb_diagnostics",
            "redis": "redis_diagnostics",
            "postgresql": "postgresql_diagnostics",
            "elasticsearch": "elasticsearch_diagnostics",
            "keycloak": "keycloak_diagnostics",
            "vault": "vault_diagnostics"
        }

    def get_failed_objects(self):
        failed_objects_file = self.args.failed_objects_file
        try:
            with open(failed_objects_file, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{failed_objects_file}' not found.")
            return []
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file '{failed_objects_file}': {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred while reading '{failed_objects_file}': {e}")
            return []

        if not isinstance(data, list):
            print(f"Error: Invalid JSON data format in '{failed_objects_file}'.")
            return []

        all_failed_entry_functions = []
        for entry in data:
            if isinstance(entry, dict) and entry['status']==2:
                all_failed_entry_functions.append(entry.get('check_entry_function', ''))
        # print("All failed entry functions",all_failed_entry_functions)
        return all_failed_entry_functions

    def get_diagnostic_commands(self):
        yaml_file = self.args.yaml_file
        try:
            with open(yaml_file, 'r') as file:
                data = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: File '{yaml_file}' not found.")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file '{yaml_file}': {e}")
            return {}

        if not isinstance(data, dict):
            print(f"Error: Invalid YAML data format in '{yaml_file}'.")
            return {}

        diagnostics_commands = {}
        if 'checks' in data and isinstance(data['checks'], dict) and 'diagnostic_commands' in data['checks']:
            for check_name, d_commands in data['checks']['diagnostic_commands'].items():
                if isinstance(d_commands, list):
                    diagnostics_commands[check_name] = d_commands
                else:
                    print(f"Error: Invalid format for diagnostics commands under '{check_name}' in '{yaml_file}'.")
        else:
            print(f"Error: 'checks->diagnostics' section not found in '{yaml_file}'.")
        # print("Diagnostic commands from yaml", diagnostics_commands)
        return diagnostics_commands

    def get_diagnostic_commands_for_failed_checks(self):
        diagnostics_commands = self.get_diagnostic_commands()
        failed_checks = self.get_failed_objects()
        diagnostic_commands_for_failed_checks = {}

        for failed_check in failed_checks:
            if failed_check in diagnostics_commands:
                diagnostic_commands_for_failed_checks[failed_check] = diagnostics_commands[failed_check]

        return diagnostic_commands_for_failed_checks

    def execute_diagnostics(self, diag_commands):
        diag_outputs = {}
        for entry_function, commands in diag_commands.items():
            for prefix, function_name in self.calling_map.items():
                if entry_function.startswith(prefix):
                    try:
                        # Fetch the function from globals based on the name
                        function = globals().get(function_name)
                        if function:
                            # Call the function with the commands
                            diag_outputs[entry_function] = function(commands)
                            print(f"Function '{function_name}' is accessible.")
                        else:
                            raise ValueError(f"Function '{function_name}' not found in the global namespace.")
                    except Exception as e:
                        print(f"Error occurred while processing '{entry_function}': {e}")
        return diag_outputs

    def write_to_yaml_file(self, data, file_path):
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    def main(self):
        if not os.path.exists(self.args.output_dir_path):
            print(f"ERROR: Output directory {self.args.output_dir_path} does not exist!")
            sys.exit(1)
        
        diag_commands = self.get_diagnostic_commands_for_failed_checks()

        if not diag_commands:
            print("Skipping Diagnostics: No diagnostic command found. You can define them in the YAML configuration file")
            return 

        diag_outputs = self.execute_diagnostics(diag_commands)

        if diag_outputs:
            diag_file = os.path.join(self.args.output_dir_path, 'diagnostics.yaml')
            self.write_to_yaml_file(diag_outputs, diag_file)
        else:
            print("WARNING: Nothing to write, diagnostic outputs are empty!")


def main(args):
    parser = argparse.ArgumentParser(description="Diagnostic Script for unskript-ctl")
    parser.add_argument("--yaml-file", '-y', help="Path to YAML file", required=True)
    parser.add_argument("--failed-objects-file", '-f', help="Path to failed objects file", required=True)
    parser.add_argument("--output-dir-path", '-o', help="Path to output directory", required=True)
    ap = parser.parse_args(args)

    diagnostics_script = DiagnosticsScript(ap)
    diagnostics_script.main()

if __name__ == "__main__":
    main(sys.argv[1:])