##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from unskript.legos.utils import parseARN
from typing import List
import pprint


class InputSchema(BaseModel):
    arn: str = Field(
        title='Target Group ARN',
        description='ARN of the Target Group.')


def aws_target_group_list_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_target_group_list_instances(handle, arn: str) -> List:
    """aws_target_group_list_instances List instances in a target group.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type arn: string
        :param arn: ARN of the Target Group.

        :rtype: List of instances with their IPs.
    """
    # Input param validation.
    # Get the region for the target group.
    parsedArn = parseARN(arn)
    elbv2Client = handle.client('elbv2', region_name=parsedArn['region'])
    ec2Client = handle.client('ec2', region_name=parsedArn['region'])
    try:
        targetHealthResponse = elbv2Client.describe_target_health(
            TargetGroupArn=arn
        )
    except Exception as e:
        print(f'Hit exception getting the instance list: {str(e)}')
        raise e

    instancesInfo = []
    for ins in targetHealthResponse["TargetHealthDescriptions"]:
        try:
            privateIP = get_instance_private_ip(ec2Client, ins['Target']['Id'])
        except Exception as e:
            continue
        instanceInfo = {
            'InstanceID': ins['Target']['Id'],
            'PrivateIP': privateIP
        }
        instancesInfo.append(instanceInfo)

    return instancesInfo


def get_instance_private_ip(ec2Client, instanceID: str) -> str:
    try:
        resp = ec2Client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-id',
                    'Values': [instanceID]
                }
            ]
        )
    except Exception as e:
        print(f'Failed to get instance details for {instanceID}, err: {str(e)}')
        raise e

    return resp['Reservations'][0]['Instances'][0]['PrivateIpAddress']
