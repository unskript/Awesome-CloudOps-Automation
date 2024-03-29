##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import List
from pydantic import BaseModel, Field
import os
import subprocess


class InputSchema(BaseModel):
    commands: list = Field(
        title='List of mongosh commands',
        description='List of mongosh commands'
    )


def mongodb_run_cli_cmd_printer(output):
    if not output:
        print("No output generated")
        return
    
    for result_dict in output:
        for command, cmd_output in result_dict.items():
            print(f"Mongosh Command: {command}\nOutput: {cmd_output}\n")


def mongodb_run_cli_cmd(handle, commands:list) -> List:
    """
    mongodb_run_cli_cmd runs mongocli command with command as the parameter

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :type commands: list
    :param commands: List of mongosh commands 

    :rtype: String output from the commands
    
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
                output = result.stdout
                command_outputs.append({command: output})
        except Exception as e:
            command_outputs.append({command: f"Exception: {str(e)}"})

    return command_outputs
