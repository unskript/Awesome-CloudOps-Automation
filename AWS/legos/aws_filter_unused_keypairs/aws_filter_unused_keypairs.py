##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List
from unskript.connectors.aws import aws_get_paginator
import pprint

class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_filter_unused_keypairs_printer(output):
    if output is None:
        return
    pprint.pprint({"Instances": output})


def aws_filter_unused_keypairs(handle, region: str) -> List:
    """aws_filter_unused_keypairs Returns an array of KeyPair.

        :type handle: object
        :param handle: Object returned from task.validate(...).
        
        :type region: object
        :param region: Object containing global params for the notebook.

        :rtype: Array of instances matching tags.
    """
    key_pairs_all = []
    used_key_pairs = []
    ec2Client = handle.client('ec2', region_name=region)

    # List the key pairs in the selected region
    key_pairs_all = list(map(lambda i: i['KeyName'], ec2Client.describe_key_pairs()['KeyPairs']))

    # Get group of EC2 instances.
    res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")
    for reservation in res:
        for keypair in reservation['Instances']:
            if 'KeyName'in keypair and keypair['KeyName'] not in used_key_pairs:
                used_key_pairs.append(keypair['KeyName'])

    # Compaire key_pairs_all and used_key_pairs list
    result = []
    for key in key_pairs_all:
        if key not in used_key_pairs:
            result.append(key)
    return result