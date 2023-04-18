##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Dict
import pprint


class InputSchema(BaseModel):
    log_group_name: str = Field(
        title='Log Group Name',
        description='Name of the log group.')
    log_stream_name: str = Field(
        title='Log Stream Name',
        description='Name of the log stream.')
    region: str = Field(
        title='Region',
        description='AWS Region')


def aws_delete_log_stream_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_delete_log_stream(handle, log_group_name: str, log_stream_name: str, region: str) -> Dict:
    """aws_delete_log_stream Deletes a log stream.
    
        :type log_group_name: string
        :param log_group_name: Name of the log group.
        
        :type log_stream_name: string
        :param log_stream_name: Name of the log stream.

        :type region: string
        :param region: AWS Region.

        :rtype: Dict with the deleted log stream info.
    """
    try:
        log_Client = handle.client('logs', region_name=region)
        response = log_Client.delete_log_stream(
            logGroupName=log_group_name,
            logStreamName=log_stream_name)
        return response
    except Exception as e:
        raise Exception(e)