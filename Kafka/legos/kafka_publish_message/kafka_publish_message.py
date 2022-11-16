##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
import pprint


pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    topic: str = Field(
        title='Topic Name',
        description='Name of the Kafka topic, the message need to be sent on.'
    )
    message: str = Field(
        title='Message',
        description='Message to be sent.'
    )


def kafka_publish_message_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def kafka_publish_message(handle, topic: str, message: str) -> str:
    
    """kafka_publish_message publish messages

        :type topic: str
        :param topic: Name of the Kafka topic, the message need to be sent on.

        :type message: str
        :param message: Message to be sent.

        :rtype: string
    """
    try:
        res = handle.send(topic, message.encode())

    except Exception as e:
        print(f'Publish message failed, err: {e}')
        raise e

    return res
