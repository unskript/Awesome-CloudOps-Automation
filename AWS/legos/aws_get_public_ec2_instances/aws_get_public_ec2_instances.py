##
##  Copyright (c) 2022 unSkript, Inc
##  All rights reserved.
##  Written by Doug Sillars (and a little help from ChatGPT)

from typing import List, Dict
from pydantic import BaseModel, Field
import pprint
from datetime import datetime, timezone, timedelta
from unskript.connectors.aws import aws_get_paginator



class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')



from beartype import beartype
@beartype
def aws_get_public_ec2_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


@beartype
def aws_get_public_ec2_instances(handle, region: str) -> Dict:


    ec2Client = handle.client('ec2', region_name=region)

    res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")


    result={}
        # Iterate through the list of instances
    for reservation in res:
         for instance in reservation['Instances']:
            #print("instance",instance)
            instance_id = instance['InstanceId']
            public_DNS = instance['PublicDnsName']
            if len(public_DNS)>0:
                public_ip = instance['PublicIpAddress']
                result[instance_id] = {"public DNS": public_DNS,"public IP":public_ip}
    return(result)
