##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict
import pprint
from beartype import beartype


class InputSchema(BaseModel):
    instance_id: str = Field(
        title='Instance Id',
        description='ID of the instance.')
    region: str = Field(
        title='Region',
        description='AWS Region of the instance.')
        

def aws_get_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


@beartype
def aws_get_instance_details(
    handle,
    instance_id: str,
    region: str,
) -> Dict:

    ec2client = handle.client('ec2', region_name=region)
    instances = []
    response = ec2client.describe_instances(
        Filters=[{"Name": "instance-id", "Values": [instance_id]}])
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append(instance)

    return instances[0]
