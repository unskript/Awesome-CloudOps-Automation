##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
import pprint
from typing import List


class InputSchema(BaseModel):
    dns_name: str = Field(
        title='Private DNS Name',
        description='Private DNS Name.')
    region: str = Field(
        title='Region',
        description='AWS Region of the resource.')


def aws_get_instance_detail_with_private_dns_name_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_instance_detail_with_private_dns_name(
        handle,
        dns_name: str,
        region: str) -> List:
    """aws_get_instance_detail_with_private_dns_name Returns an array of private dns name.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type dns_name: string
        :param dns_name: Private DNS Name.

        :type region: string
        :param region: AWS Region of the resource.

        :rtype: Returns an array of private dns name
    """

    ec2Client = handle.client('ec2', region_name=region)

    res = aws_get_paginator(ec2Client, "describe_instances", "Reservations",
                            Filters=[{"Name": 'private-dns-name', "Values": [dns_name]}])
    instances = []
    for reservation in res:
        for instance in reservation['Instances']:
            instances.append(instance)

    return instances
