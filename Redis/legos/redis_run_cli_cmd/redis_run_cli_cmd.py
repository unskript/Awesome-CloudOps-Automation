##
##  Copyright (c) 2024 unSkript, Inc
##  All rights reserved.
##
from typing import List
from pydantic import BaseModel, Field
import os
import subprocess


class InputSchema(BaseModel):
    commands: list = Field(
        title='List of redis-cli commands',
        description='List of redis-cli commands. Example- ["info","--bigkeys"]'
    )


def redis_run_cli_cmd_printer(output):
    if not output:
        print("No output generated")
        return
    
    for result_dict in output:
        for command, cmd_output in result_dict.items():
            print(f"Redis Command: {command}\nOutput: {cmd_output}\n")


def redis_run_cli_cmd(handle, commands:list) -> List:
    """
    redis_run_cli_cmd runs redis-cli command with command as the parameter

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :type commands: list
    :param commands: List of redis commands 

    :rtype: String output from the commands
    
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
                output = result.stdout
                command_outputs.append({command: output})
        except Exception as e:
            command_outputs.append({command: f"Exception: {str(e)}"})
    return command_outputs
