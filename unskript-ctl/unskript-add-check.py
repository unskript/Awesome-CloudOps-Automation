"""This file implements add check functionality"""
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
from jinja2 import Environment, FileSystemLoader

#from creds_ui import main as ui
from argparse import ArgumentParser

class CreateCheck():
    def __init__(self):
        #Check if this is being run from the top of the directory which has actions directory.
        current_directory = os.getcwd()
        action_dir_path = current_directory + '/actions'
        if os.path.exists(action_dir_path) is False:
            print("Please run it from the top of the directory, where actions directory exists")
            return

        mainParser = ArgumentParser(prog='unskript-add-check')
        mainParser.add_argument('-t', '--type', help='Type of check', choices=[
         'AWS',
         'K8S',
         'GCP',
         'ELASTICSEARCH',
         'REDIS',
         'POSTGRESQL',
         'MONGODB',
         'KAFKA'])
        mainParser.add_argument('-n', '--name', help='Short name separated by underscore. For eg: aws_list_public_buckets')
        mainParser.add_argument('-d', '--description', help='Detailed description about the check.')

        args = mainParser.parse_args()
        json_data = {}
        json_data['action_title'] = args.name
        json_data['action_description'] = args.description
        json_data['action_type'] = "LEGO_TYPE_" + args.type
        json_data['action_entry_function'] = args.name
        json_data['action_needs_credential'] = True
        json_data['action_output_type'] = "ACTION_OUTPUT_TYPE_LIST"
        json_data['action_is_check'] = True
        json_data['action_supports_iteration'] = True
        json_data['action_supports_poll'] = True

        custom_dir = action_dir_path + "/" + args.name
        Path(custom_dir).mkdir(parents=True, exist_ok=True)
        # Generate .json file
        try:
            with open(custom_dir + "/" + args.name + ".json", "w") as f:
                f.write(json.dumps(json_data, indent=2))
        except Exception as e:
            raise Exception(f"Unable to create JSON File {e}")

        # Generate __init__.py file
        try:
            file = open( custom_dir + "/" + "__init__.py","w")
            file.close()
        except Exception as e:
            print(f"Unable to create __init__.py File {e}")

        AWESOME_DIRECTORY = "Awesome-CloudOps-Automation"
        environment = Environment(loader=FileSystemLoader(current_directory + "/" + AWESOME_DIRECTORY + "/unskript-ctl/templates/"))
        template = environment.get_template("check.py.template")

        content = template.render({"check_function_name": args.name})
        try:
            with open(custom_dir + "/" + args.name + ".py", "w") as f:
                f.write(content)
        except Exception as e:
            raise Exception(f"Unable to create .py File {e}")

        template = environment.get_template("check_test.py.template")

        content = template.render({
            "check_function_name": args.name,
            "check_type_upper_case": args.type.upper(),
            "check_type": args.type,
            })
        try:
            with open(custom_dir + "/" + "test_" + args.name + ".py", "w") as f:
                f.write(content)
        except Exception as e:
            raise Exception(f"Unable to create test .py File {e}")


if __name__ == '__main__':
    CreateCheck()
