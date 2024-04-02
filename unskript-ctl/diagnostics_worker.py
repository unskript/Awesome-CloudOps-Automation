##
##  Copyright (c) 2024 unSkript, Inc
##  All rights reserved.
##
import os
import subprocess


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
            print(f"Mongosh Command: {command}\nOutput: {cmd_output}\n")
    return command_outputs

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
            print(f"K8S Command: {command}\nOutput: {cmd_output}\n")
    return command_outputs

def redis_diagnostics(commands:list):
    """
    redis_diagnostics runs redis-cli command with command as the parameter

    """
    REDIS_HOSTNAME = os.getenv('REDIS_HOSTNAME', 'localhost')
    REDIS_PORT = os.getenv('REDIS_PORT', '6379')

    command_outputs = []

    for command in commands:
        cmd = [
        "redis-cli",
        "-h", REDIS_HOSTNAME,
        "-p", REDIS_PORT,
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
            print(f"Redis Command: {command}\nOutput: {cmd_output}\n")
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
            print(f"Postgres Command: {command}\nOutput: {cmd_output}\n")
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
            print(f"Elasticsearch curl command: {command}\nOutput: {cmd_output}\n")
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
            print(f"Keycloak curl command: {command}\nOutput: {cmd_output}\n")
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
            print(f"Vault Command: {command}\nOutput: {cmd_output}\n")
    return command_outputs
