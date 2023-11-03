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
import add_creds
import json
import ruamel.yaml
import sys

UNSKRIPT_CTL_CONFIG_FILE="config/unskript_ctl_config.yaml"

# Add credentials details to the config file based on the credential schemas
def generate_credentials(config_file):
    try:
        schema_json = json.loads(add_creds.credential_schemas)
    except Exception as e:
        print(f"Exception occured {e}")
        return
    yaml = ruamel.yaml.YAML()
    with open(config_file) as fp:
        unskript_ctl_config_yaml_data = yaml.load(fp)
        credentials_details = {}
        for schema in schema_json:
            credential_name = schema.get('title').replace('Schema', '').lower()
            properties = schema.get('properties', {})
            params_info = {"name": credential_name+"creds", "enable": False}
            discriminator = ""
            for prop, prop_info in properties.items():
                if prop_info.get('discriminator') is not None:
                    discriminator = prop_info.get('discriminator')
                    params_info['discriminator'] = discriminator
                    continue
                prop_value = None
                if prop_info.get('default') is not None:
                    prop_value = prop_info.get('default')
                else:
                    prop_value = get_default_value_for_param(prop_info.get('type'))
                params_info[prop] = prop_value
            if schema.get('definitions') is not None:
                    definitions = schema.get('definitions')
                    for schema_name, schema_definition in definitions.items():
                        schema_properties = schema_definition.get('properties', {})
                        schema_params_info = {"enable": False}
                        for schema_prop, schema_prop_info in schema_properties.items():
                            if schema_prop == discriminator and len(schema_prop_info.get('enum')) == 1:
                                schema_params_info[discriminator] = schema_prop_info.get('enum')[0]
                                continue
                            schema_prop_value = None
                            if schema_prop_info.get('default') is not None:
                                schema_prop_value = schema_prop_info.get('default')
                            else:
                                schema_prop_value = get_default_value_for_param(schema_prop_info.get('type'))
                            schema_params_info[schema_prop] = schema_prop_value
                        params_info[schema_name] = schema_params_info
            credentials_details[credential_name] = [params_info]
        unskript_ctl_config_yaml_data['credential'] = credentials_details
        # Redirect stdout to a file. Dumping yaml to stdout ensures formatting and comments are retained
        with open(config_file, 'w') as output_file:
            sys.stdout = output_file
            yaml.dump(unskript_ctl_config_yaml_data, sys.stdout)
    # Reset stdout to the original sys.stdout
    sys.stdout = sys.__stdout__

def get_default_value_for_param(parameter_type) -> any:
    default_value = ""
    if parameter_type == "number":
        default_value = 0
    if parameter_type == "boolean":
        default_value = False
    if parameter_type == "array":
        default_value = []
    if parameter_type == "object":
        default_value = {}
    return default_value

if __name__ == "__main__":
    generate_credentials(UNSKRIPT_CTL_CONFIG_FILE)
