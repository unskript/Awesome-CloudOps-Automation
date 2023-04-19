##  Copyright (c) 2023 unSkript, Inc
## Written by Doug Sillars and ChatGPT
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
import pprint
from datetime import datetime, timezone

from beartype import beartype


class InputSchema(BaseModel):
    instance: str = Field(
        title='EC2 Instance',
        description='Name of the EC2 Instance.')
    tag_key: str = Field(
        title='Tag Key',
        description='Key of the tag to be added.')
    tag_value: str = Field(
        title='Tag Value',
        description='Value of the tag to be added.')
    region: str = Field(
        title='Region',
        description='Name of the AWS where the instance is located.')





@beartype
def aws_tag_ec2_instance_printer(output):
    if output is None:
        return
    pprint.pprint(output)


@beartype
def aws_tag_ec2_instance(handle, instance: str, tag_key: str, tag_value: str, region:str) -> Dict:


    ec2 = handle.client('ec2', region_name=region)
    res = ec2.create_tags(Resources=[instance], Tags=[{'Key': tag_key, 'Value': tag_value}])


    return(res)
