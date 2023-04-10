##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
import pprint

class InputSchema(BaseModel):
    listener_arn: str = Field(
        title='ListenerArn',
        description='listener ARNs.')

    region: str = Field(
        title='Region',
        description='AWS Region of the ALB listeners.')
        
def aws_modify_listener_for_http_redirection_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_modify_listener_for_http_redirection(handle, listener_arn: str, region: str) -> List:
    """aws_modify_listener_for_http_redirection List of Dict with modified listener info.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type listener_arn: string
        :param listener_arn: List of listenerArn.

        :type region: string
        :param region: Region to filter ALB listeners.

        :rtype: List of Dict with modified ALB listeners info.
    """
    listner_config = [{
                        "Type": "redirect",
                        "Order": 1,
                        "RedirectConfig": {
                            "Protocol": "HTTPS",
                            "Host": "#{host}",
                            "Query": "#{query}",
                            "Path": "/#{path}",
                            "Port": "443",
                            "StatusCode": "HTTP_302"}}]
    result = []
    try:
        ec2Client = handle.client('elbv2', region_name=region)
        response = ec2Client.modify_listener(ListenerArn=listener_arn,
                                             DefaultActions=listner_config)
        result.append(response)

    except Exception as error:
        result.append(error)

    return result