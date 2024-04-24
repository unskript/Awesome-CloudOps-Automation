##
##  Copyright (c) 2024 unSkript, Inc
##  All rights reserved.
##
import os
import subprocess
import json
from unskript_ctl_factory import UctlLogger
import yaml


logger = UctlLogger('UnskriptDiagnostics')


def append_to_yaml_file(data, file_path):
    if not data:
        return
    try:
        with open(file_path, 'a') as file:
            yaml.safe_dump(data, file, default_flow_style=False, allow_unicode=True)
    except Exception as e:
        logger.error(f"Failed to write data to {file_path}: {e}")

def mongodb_diagnostics(commands:list):
    """
    mongodb_diagnostics runs mongocli command with command as the parameter
    """
    MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
    MONGODB_HOSTNAME = os.getenv('MONGODB_HOSTNAME', 'localhost')
    MONGODB_PORT = int(os.getenv('MONGODB_PORT', 27017))

    # Format the connection string for mongosh
    connection_string = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOSTNAME}:{MONGODB_PORT}"
    command_outputs = []

    for command in commands:
        cmd = [
            "mongosh",
            connection_string,
            "--quiet",
            "--eval",
            command
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stderr:
                command_outputs.append({command: f"Error: {result.stderr.strip()}"})
            else:
                output = result.stdout.splitlines()
                command_outputs.append({command: output})
        except Exception as e:
            command_outputs.append({command: f"Exception: {str(e)}"})

    for result_dict in command_outputs:
        for command, cmd_output in result_dict.items():
            logger.debug("\nMongodb Diagnostics")
            logger.debug(f"Mongosh Command: {command}\nOutput: {cmd_output}\n")
    return command_outputs

def fetch_logs(namespace, pod, container, output_path):
    """
    Fetches logs and previous logs for a specified container in a pod and writes directly to a file with headers and separators.
    """
    logs_file_path = os.path.join(output_path, 'logs.txt')
    separator = f"\n{'=' * 40}\n"
    header = f"Logs for Namespace: {namespace}, Pod: {pod}, Container: {container}\n"
    header_previous = f"Previous Logs for Namespace: {namespace}, Pod: {pod}, Container: {container}\n"

    try:
        # Write header and current logs to file
        with open(logs_file_path, 'a') as f:
            f.write(separator + header)
            subprocess.run(["kubectl", "logs", "--namespace", namespace, pod, "-c", container],
                           stdout=f, stderr=f, text=True, check=False)

        # Write header for previous logs and the logs themselves to file
        with open(logs_file_path, 'a') as f:
            f.write(separator + header_previous)
            subprocess.run(["kubectl", "logs", "--namespace", namespace, pod, "-c", container, "--previous"],
                           stdout=f, stderr=f, text=True, check=False)

    except Exception as e:
        logger.error(f"Failed to fetch and write logs for {namespace}/{pod}/{container}: {e}")

def fetch_pod_logs_not_running(output_path):
    logger.debug("\nK8s Diagnostics: Fetching logs for pods not running")
    cmd = ["kubectl", "get", "pods", "--all-namespaces", "-o", "json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    pods = json.loads(result.stdout)['items']
    
    for pod in pods:
        namespace = pod['metadata']['namespace']
        name = pod['metadata']['name']
        status = pod['status']['phase']
        if status != "Running":
            # logger.debug(f"Fetching logs for Pod: {name} in Namespace: {namespace} (Not Running)")
            containers = [c['name'] for c in pod['spec'].get('initContainers', []) + pod['spec'].get('containers', [])]
            for container in containers:
                fetch_logs(namespace, name, container, output_path)

def fetch_pod_logs_high_restarts(output_path):
    logger.debug("\nK8s Diagnostics: Fetching logs for pods with high restarts")
    cmd = ["kubectl", "get", "pods", "--all-namespaces", "-o", "json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    pods = json.loads(result.stdout)['items']
    
    for pod in pods:
        namespace = pod['metadata']['namespace']
        name = pod['metadata']['name']
        pod_status = pod['status'].get('containerStatuses', [])
        for container_status in pod_status:
            if container_status['restartCount'] > 25:
                container_name = container_status['name']
                # logger.debug(f"Fetching logs for Pod: {name}, Container: {container_name} in Namespace: {namespace} with high restarts")
                fetch_logs(namespace, name, container_name, output_path)

def k8s_diagnostics(commands:list):
    """
    k8s_diagnostics runs kubectl command

    """
    command_outputs = []

    for command in commands:
        cmd_list = command.split()
        try:
            result = subprocess.run(cmd_list, capture_output=True, text=True)
            if result.stderr:
                command_outputs.append({command: f"Error: {result.stderr.strip()}"})
            else:
                output = result.stdout.splitlines()
                command_outputs.append({command: output})
        except Exception as e:
            command_outputs.append({command: f"Exception: {str(e)}"})

    for result_dict in command_outputs:
        for command, cmd_output in result_dict.items():
            logger.debug("\n Kubernetes Diagnostics")
            logger.debug(f"K8S Command: {command}\nOutput: {cmd_output}\n")
    return command_outputs

def redis_diagnostics(commands:list):
    """
    redis_diagnostics runs redis-cli command with command as the parameter

    """
    REDIS_HOSTNAME = os.getenv('REDIS_HOSTNAME', 'localhost')
    REDIS_PORT = os.getenv('REDIS_PORT', '6379')
    REDIS_USERNAME = os.getenv('REDIS_USERNAME')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

    if REDIS_USERNAME and REDIS_PASSWORD:
        redis_uri = f"redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOSTNAME}:{REDIS_PORT}"
    elif REDIS_PASSWORD:
        redis_uri = f"redis://:{REDIS_PASSWORD}@{REDIS_HOSTNAME}:{REDIS_PORT}"
    else:
        redis_uri = f"redis://{REDIS_HOSTNAME}:{REDIS_PORT}"

    command_outputs = []

    for command in commands:
        cmd = [
            "redis-cli",
            "-u", redis_uri,
            command
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stderr:
                command_outputs.append({command: f"Error: {result.stderr.strip()}"})
            else:
                output = result.stdout.splitlines()
                command_outputs.append({command: output})
        except Exception as e:
            command_outputs.append({command: f"Exception: {str(e)}"})
    for result_dict in command_outputs:
        for command, cmd_output in result_dict.items():
            logger.debug("\nRedis Diagnostics")
            logger.debug(f"Redis Command: {command}\nOutput: {cmd_output}\n")
    return command_outputs

def postgresql_diagnostics(commands:list):
    """
    postgresql_diagnostics runs psql command with query as the parameter
    """
    POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOSTNAME = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_DB_NAME =os.getenv('POSTGRES_DB_NAME',"")

    connection_string = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"
    command_outputs = []

    for command in commands:
        cmd = [
            "psql",
            connection_string,
            "-c",
            command
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stderr:
                command_outputs.append({command: f"Error: {result.stderr.strip()}"})
            else:
                output = result.stdout.splitlines()
                command_outputs.append({command: output})
        except Exception as e:
            command_outputs.append({command: f"Exception: {str(e)}"})

    for result_dict in command_outputs:
        for command, cmd_output in result_dict.items():
            logger.debug("\nPostgresql Diagnostics")
            logger.debug(f"Postgres Command: {command}\nOutput: {cmd_output}\n")
    return command_outputs

def elasticsearch_diagnostics(commands: list) -> list:
    """
    Runs Elasticsearch diagnostics commands via curl.

    """
    ELASTICSEARCH_HOSTS = os.getenv('ELASTICSEARCH_HOSTS', 'http://localhost:9200')

    command_outputs = []

    for command in commands:
        # Ensure the command does not end with a slash as it might cause issues with curl
        if command.endswith('/'):
            command = command[:-1]
        cmd = f"curl -sS -X GET {ELASTICSEARCH_HOSTS}/{command}"
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            if result.stderr:
                command_outputs.append({command: f"Error: {result.stderr.strip()}"})
            else:
                output = result.stdout.splitlines()
                command_outputs.append({command: output})
        except Exception as e:
            command_outputs.append({command: f"Exception: {str(e)}"})

    for result_dict in command_outputs:
        for command, cmd_output in result_dict.items():
            logger.debug("\nElasticsearch Diagnostics")
            logger.debug(f"Elasticsearch curl command: {command}\nOutput: {cmd_output}\n")
    return command_outputs

def keycloak_diagnostics(commands: list):
    """
    Runs Keycloak diagnostics commands via curl.
    """
    keycloak_url = os.getenv('KEYCLOAK_URL', 'http://localhost/auth/')
    keycloak_realm = os.getenv('KEYCLOAK_REALM', 'master')
    command_outputs = []
    
    openid_config_url = f"{keycloak_url.rstrip('/')}/realms/{keycloak_realm}/"

    for command in commands:
        cmd = f"curl -k -s \"{openid_config_url}{command}\""
    
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            if result.stderr:
                command_outputs.append({command: f"Error: {result.stderr.strip()}"})
            else:
                output = result.stdout.splitlines()
                command_outputs.append({command: output})
        except Exception as e:
            command_outputs.append({command: f"Exception: {str(e)}"})

    for result_dict in command_outputs:
        for command, cmd_output in result_dict.items():
            logger.debug("\nKeycloak Diagnostics")
            logger.debug(f"Keycloak curl command: {command}\nOutput: {cmd_output}\n")
    return command_outputs

def vault_diagnostics(commands: list):
    """
    vault_diagnostics runs Vault CLI commands with the command as the parameter.

    """
    VAULT_ADDR = os.getenv('VAULT_ADDR', 'http://localhost:8200')
    VAULT_TOKEN = os.getenv('VAULT_TOKEN')
    
    command_outputs = []

    for command in commands:
        command_parts = command.split()
        
        cmd = [
            "vault",
        ] + command_parts 
        
        try:
            env = os.environ.copy()
            env['VAULT_ADDR'] = VAULT_ADDR
            env['VAULT_TOKEN'] = VAULT_TOKEN
            
            result = subprocess.run(cmd, capture_output=True, text=True, env=env)
            if result.stderr:
                command_outputs.append({command: f"Error: {result.stderr.strip()}"})
            else:
                output = result.stdout.splitlines()
                command_outputs.append({command: output})
        except Exception as e:
            command_outputs.append({command: f"Exception: {str(e)}"})

    for result_dict in command_outputs:
        for command, cmd_output in result_dict.items():
            logger.debug("\nVault Diagnostics")
            logger.debug(f"Vault Command: {command}\nOutput: {cmd_output}\n")
    return command_outputs
