##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List
import pprint


class InputSchema(BaseModel):
    ami_id: str = Field(
        title='AMI Id',
        description='AMI Id.')
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_launch_instance_from_ami_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_launch_instance_from_ami(handle, ami_id: str, region: str) -> List:
    """aws_launch_instance_from_ami Launch instances from a particular image.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type ami_id: string
        :param ami_id: AMI Id Information required to launch an instance.

        :type region: string
        :param region: Region to filter instances.

        :rtype: Dict with launched instances info.
    """
    ec2Client = handle.client('ec2', region_name=region)

    res = ec2Client.run_instances(ImageId=ami_id, MinCount=1, MaxCount=1)

    return res['Instances']
