##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List
from unskript.connectors.aws import aws_get_paginator
import pprint


class InputSchema(BaseModel):
    lifetime_tag: str = Field(
        title='Lifetime tag',
        description='Tag which indicates the lifecycle of instance.')

    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_filter_ec2_without_lifetime_tag_printer(output):
    if output is None:
        return
    pprint.pprint({"Instances": output})


def aws_filter_ec2_without_lifetime_tag(handle, lifetime_tag: str, region: str='') -> List:
    """aws_filter_ec2_without_lifetime_tag Returns an List of instances which not have lifetime tag.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type lifetime_tag: string
        :param lifetime_tag: Tag to filter Instances.

        :type region: string
        :param region: Used to filter the instance for specific region.

        :rtype: Array of instances which not having lifetime tag.
    """

    untagged_instances_dict={}
    ec2Client = handle.client('ec2', region_name=region)
    result_list = []
    instance_list = []
    try:
        res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")
        for reservation in res:
            for instance in reservation['Instances']:
                    tagged_instance = instance['Tags']
                    tag_keys = [tags['Key'] for tags in tagged_instance]
                    if lifetime_tag in tag_keys:
                        instance_list.append(instance['InstanceId'])
                    untagged_instances_dict["region"] = region
                    untagged_instances_dict["instances"] = instance_list
        result_list.append(untagged_instances_dict)
    except Exception as e:
        pass
    return result_list

