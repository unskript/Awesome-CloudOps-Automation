#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#

import pprint
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    aws_command: str = Field(
        title='AWS Command',
        description='AWS Command '
                    'eg "aws ec2 describe-instances"'
    )


def aws_execute_cli_command_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_execute_cli_command(handle, aws_command: str) -> str:

    result = handle.aws_cli_command(aws_command)
    if result is None or result.returncode != 0:
        print(
            f"Error while executing command ({aws_command}): {result}")
        return str()

    return result.stdout
