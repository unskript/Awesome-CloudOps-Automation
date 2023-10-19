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


from pathlib import Path
try:
    from envyaml import EnvYAML
except Exception as e:
    print("ERROR: Unable to find required yaml package to parse hooks.yaml file!")
    raise e

#logging.basicConfig(
#    level=logging.DEBUG,
#    format='%(asctime)s [%(levelname)s] - %(message)s',
#    datefmt='%Y-%m-%d %H:%M:%S',
#    filename="/tmp/"
#)

def parse_hook_yaml(hook_file: str) -> dict:
    """parse_hook_yaml: This function parses the hooks yaml file and converts the
    content as a python dictionary and returns back to the caller.
    """
    retval = {}
    if not hook_file:
        hook_file = os.path.join(os.environ.get('HOME'), 'hook.yaml')

    if os.path.exists(hook_file) == False:
        print(f"WARNING: {hook_file} Not found!")
        return retval


    # We use EnvYAML to parse the hook file and give us the
    # dictionary representation of the YAML file
    retval = EnvYAML(hook_file, strict=False)

    if not retval:
        print(f"WARNING: Hooks file content seems to be empty!")
        return retval

    return retval


def configure_credential(creds_dict: dict):
    """configure_credential: This function is used to parse through the creds_dict and
    call the add_creds.sh method to populate the respective credential json
    """
    if not creds_dict:
        print(f"ERROR: Nothing to configure credential with, found empty creds data")
        return

    creds_cmd = []
    for cred_type in creds_dict.keys():
        cred_list = creds_dict.get(cred_type)
        for cred in cred_list:
            if cred.get('enable') == False:
                continue
            creds_cmd = ['add_creds.sh', '-c', cred_type]
            for cred_key in cred:
                # Skip name and enable keys
                if cred_key in ['name', 'enable']:
                    continue
                creds_cmd.extend(['--'+cred_key, cred.get(cred_key)])
        #if cred.lower() == 'aws':
        #    aws_config = creds_dict.get(cred)
        #    access_key = creds_dict.get(cred).get('access_key')
        #    secret_access_key = creds_dict.get(cred).get('secret_access_key')
        #    if access_key.startswith('$') or secret_access_key.startswith('$'):
        #        print("One or more environment variable is not set for AWS credential")
        #        continue
        #    creds_cmd = ["add_creds.sh", "-c", "AWS", "-a", access_key, "-s", secret_access_key]
        #    break
        #elif cred.lower() == 'k8s':
        #    kubeconfig = creds_dict.get(cred).get('kubeconfig')
        #    if kubeconfig.startswith('$'):
        #        print("One or more environment variable is not set for K8S credential")
        #        continue
        #    creds_cmd = ["add_creds.sh", "-c", "K8S", "-k", kubeconfig]
        #    break
        #elif cred.lower() == 'gcp':
        #    credential_json = creds_dict.get(cred).get('credential_json')
        #    if credential_json.startswith('$'):
        #        print("One or more environment variable is not set for GCP credential")
        #        continue
        #    creds_cmd = ["add_creds.sh", "-c", "GCP", "-g", credential_json]
        #    break
        #elif cred.lower() == 'elasticsearch':
        #    server = creds_dict.get(cred).get('server')
        #    api_key = creds_dict.get(cred).get('api_key')
        #    no_verify_ssl = creds_dict.get(cred).get('no_verify_ssl')
        #    if server.startswith('$') or api_key.startswith('$') or no_verify_ssl.startswith('$'):
        #        print("One or more environment variable is not set for Elasticsearch credential")
        #        continue
        #    creds_cmd = ["add_creds.sh", "-c", "Elasticsearch", "-s", server, "-a", api_key]
        #    if no_verify_ssl:
        #        creds_cmd.append('--no-verify-certs')
        #    break
        #elif cred.lower() == 'redis':
        #    server = creds_dict.get(cred).get('server')
        #    port = creds_dict.get(cred).get('port')
        #    username = creds_dict.get(cred).get('username')
        #    password = creds_dict.get(cred).get('password')
        #    database = creds_dict.get(cred).get('database')
        #    use_ssl = creds_dict.get(cred).get('use_ssl')
        #    if server.startswith('$') or \
        #       port.startswith('$') or \
        #       username.startswith('$') or \
        #       password.startswith('$') or \
        #       database.startswith('$'):
        #        print("One or more environment variable is not set for Redis credential")
        #        continue
        #    creds_cmd = ["add_creds.sh",
        #                 "-c", "Redis",
        #                 "-s", server,
        #                 "-p", port,
        #                 "-u", username,
        #                 "-pa", password,
        #                 "-db", database]
        #    if use_ssl:
        #        creds_cmd.append('--use-ssl')
        #    break
        #elif cred.lower() == 'postgres':
        #    server = creds_dict.get(cred).get('server')
        #    port = creds_dict.get(cred).get('port')
        #    username = creds_dict.get(cred).get('username')
        #    password = creds_dict.get(cred).get('password')
        #    database = creds_dict.get(cred).get('database')
        #    if server.startswith('$') or \
        #       port.startswith('$') or \
        #       username.startswith('$') or \
        #       password.startswith('$') or \
        #       database.startswith('$'):
        #        print("One or more environment variable is not set for Postgres credential")
        #        continue
        #    creds_cmd = ["add_creds.sh",
        #                 "-c", "PostGRES",
        #                 "-s", server,
        #                 "-p", port,
        #                 "-db", database,
        #                 "-u", username,
        #                 "-pa", password]
        #    break
        #elif cred.lower() == 'mongodb':
        #    server = creds_dict.get(cred).get('server')
        #    port = creds_dict.get(cred).get('port')
        #    username = creds_dict.get(cred).get('username')
        #    password = creds_dict.get(cred).get('password')
        #    if server.startswith('$') or \
        #       port.startswith('$') or \
        #       username.startswith('$') or \
        #       password.startswith('$'):
        #        print("One or more environment variable is not set for MongoDB credential")
        #        continue
        #    creds_cmd = ["add_creds.sh",
        #                 "-c", "MongoDB",
        #                 "-s", server,
        #                 "-p", port,
        #                 "-u", username,
        #                 "-pa", password]
        #    break
        #elif cred.lower() == 'kafka':
        #    broker = creds_dict.get(cred).get('broker')
        #    username = creds_dict.get(cred).get('username')
        #    password = creds_dict.get(cred).get('password')
        #    zookeeper = creds_dict.get(cred).get('zookeeper')
        #    if broker.startswith('$') or \
        #       zookeeper.startswith('$') or \
        #       username.startswith('$') or \
        #       password.startswith('$'):
        #        print("One or more environment variable is not set for Kafka credential")
        #        continue
        #    creds_cmd = ["add_creds.sh",
        #                 "-c", "Kafka",
        #                 "-b", broker,
        #                 "-u", username,
        #                 "-p", password,
        #                 "-z", zookeeper]
        #    break
        #elif cred.lower() == 'rest':
        #    base_url = creds_dict.get(cred).get('base_url')
        #    username = creds_dict.get(cred).get('username')
        #    password = creds_dict.get(cred).get('password')
        #    headers = creds_dict.get(cred).get('headers')
        #    if base_url.startswith('$') or \
        #       username.startswith('$') or \
        #       password.startswith('$') or \
        #       headers.startswith('$'):
        #        print("One or more environment variable is not set for REST credential")
        #        continue
        #    creds_cmd = ["add_creds.sh",
        #                 "-c", "REST",
        #                 "-b", base_url,
        #                 "-u", username,
        #                 "-p", password,
        #                 "-h", headers]
        #    break
        #elif cred.lower() == 'vault':
        #    url = creds_dict.get(cred).get('url')
        #    token = creds_dict.get(cred).get('token')
        #    if url.startswith('$') or \
        #       token.startswith('$'):
        #        print("One or more environment variable is not set for Vault credential")
        #        continue
        #    creds_cmd = ["add_creds.sh",
        #                 "-c", "Vault",
        #                 "-u", url,
        #                 "-t", token]
        #    break
        #elif cred.lower() == 'keycloak':
        #    server_url = creds_dict.get(cred).get('server_url')
        #    realm = creds_dict.get(cred).get('realm')
        #    client_id = creds_dict.get(cred).get('client_id')
        #    username = creds_dict.get(cred).get('username')
        #    password = creds_dict.get(cred).get('password')
        #    client_secret = creds_dict.get(cred).get('client_secret')
        #    no_verify_certs = creds_dict.get(cred).get('no_verify_certs')
        #    if server_url.startswith('$') or \
        #       realm.startswith('$') or  \
        #       client_id.startswith('$') or  \
        #       username.startswith('$') or  \
        #       password.startswith('$') or  \
        #       client_secret.startswith('$'):
        #        print("One or more environment variable is not set for Keycloak credential")
        #        continue
        #    creds_cmd = ["add_creds.sh",
        #                 "-c", "Keycloak",
        #                 "-su", server_url,
        #                 "-r", realm,
        #                 "-c", client_id,
        #                 "-u", username,
        #                 "-p", password,
        #                 "-cs", client_secret]
        #    if no_verify_certs:
        #        creds_cmd.append('--no-verify-certs')
        #    break
        else:
            print(f"WARNING: Option not implemented {cred}")

    if creds_cmd:
        print(f"CREDS CMD is {creds_cmd}")
        result = subprocess.run(creds_cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"ERROR: Cannot add_creds did not succeed: {result.stdout} {result.stderr}")
            return
        print("Credential programming was successful")
    else:
        print("ERROR: No Credential was programmed")

    return



def main():
    """main: This is the main function that gets called by the start.sh function
    to parse the unskript_ctl_config.yaml file and program credential and schedule as configured
    """
    retval = parse_hook_yaml('./config/unskript_ctl_config.yaml')

    configure_credential(retval.get('credential'))


if __name__ == '__main__':
    main()