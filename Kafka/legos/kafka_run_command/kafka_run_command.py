#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#

from pydantic import BaseModel, Field
import pprint


pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    kafka_command: str = Field(
        title='Kafka Command',
        description='Kafka command. '
                    'Eg. kafka-topics.sh --list --exclude-internal'
    )


def kafka_run_command_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def kafka_run_command(handle, kafka_command: str) -> str:
    """kafka_run_command run command

        :type kafka_command: str
        :param kafka_command: Kafka command.

        :rtype: string
    """

    assert(kafka_command.startswith("kafka"))

    result = handle.run_native_cmd(kafka_command)
    return result
