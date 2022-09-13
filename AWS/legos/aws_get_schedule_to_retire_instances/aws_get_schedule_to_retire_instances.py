##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from pydantic import BaseModel, Field
from typing import List
import pprint
from beartype import beartype


class InputSchema(BaseModel):
    instance_ids: list = Field(
        title='Instance IDs',
        description='List of Instances.')
    region: str = Field(
        title='Region',
        description='AWS Region.')


@beartype
def aws_get_schedule_to_retire_instances(
    handle,
    instance_ids: list,
    region: str,
) -> List:

    ec2client = handle.client('ec2', region_name=region)
    instances = []
    response = ec2client.describe_instance_status(
        Filters=[
        {
            'Name': 'event.code',
            'Values': ['instance-retirement']}],
        InstanceIds=instance_ids)

    for instance in response['InstanceStatuses']:
        instance_id = instance['InstanceId']
        instances.append(instance_id)

    return instances


def aws_get_schedule_to_retire_instances_printer(output):
    if output is None:
        return
    pprint.pprint({"Instances": output})