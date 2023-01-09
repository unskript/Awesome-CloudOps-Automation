##  Copyright (c) 2022 unSkript, Inc
##  All rights reserved.
##
## written by Doug Sillars with the aid of ChatGPT
##read the blog https://unskript.com/will-ai-replace-us-using-chatgpt-to-create-python-actions-for-unskript/
##

from typing import List, Dict
from pydantic import BaseModel, Field
import pprint
from datetime import datetime, timezone
from unskript.connectors.aws import aws_get_paginator
from beartype import beartype
@beartype
def aws_get_ec2_instance_age_printer(output):
    if output is None:
        return
    pprint.pprint(output)

class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region of the ECS service')



@beartype
def aws_get_ec2_instance_age(handle, region: str) -> Dict:


    ec2Client = handle.client('ec2', region_name=region)
    res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")

    # Get the current time
    now = datetime.now(timezone.utc)
    result={}
    # Iterate through the list of instances
    for reservation in res:
        for instance in reservation['Instances']:
            # Get the instance ID and launch time
            instance_id = instance['InstanceId']
            launch_time = instance['LaunchTime']

            # Calculate the age of the instance
            age = now - launch_time

            # Print the instance ID and age
            ageText = f"Instance {instance_id} is {age.days} days old"
            ageDict = {instance_id: age.days}
            print(ageText)
            result[instance_id] = age.days
    return(result)

task = Task(Workflow())
task.configure(credentialsJson='''{
    "credential_name": "DevRole",
    "credential_type": "CONNECTOR_TYPE_AWS",
    "credential_id": "0b438eba-0627-4f6d-b998-a4c604f20e3c"
}''')
task.configure(inputParamsJson='''{
    "region": "\\"us-west-2\\""
    }''')
(err, hdl, args) = task.validate(vars=vars())
if err is None:
    task.execute(aws_get_ec2_instance_age, lego_printer=aws_get_ec2_instance_age_printer, hdl=hdl, args=args)