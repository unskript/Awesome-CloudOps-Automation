##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, List
from unskript.legos.utils import parseARN
import pprint


class InputSchema(BaseModel):
    arn: str = Field(
        title='Loadbalancer Name (Classic) or ARN (ALB/NLB)',
        description='Name of the classic loadbalancer or ARN of the ALB/NLB. Classic loadbalancer dont have ARN.')
    region: Optional[str] = Field(
        title='Region of the Classic Loadbalancer',
        description='Region of the Classic loadbalancer. You dont need to fill this for ALB/NLB.'
    )
    classic: bool = Field(
        False,
        title='Classic Loadbalancer',
        description='Check if the loadbalancer is Classic. By default, its false.'
    )


def aws_loadbalancer_list_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_loadbalancer_list_instances(handle, arn: str, region: str = None, classic: bool = False) -> List:
    """aws_get_unhealthy_instances returns array of instances

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type arn: string
        :param arn: Name of the classic loadbalancer or ARN of the ALB/NLB.

        :type classic: bool
        :param classic: Check if the loadbalancer is Classic.

        :type region: string
        :param region: Region of the Classic loadbalancer.

        :rtype: Returns array of instances
    """
    instancesInfo = []
    try:
        if classic == False:
            parsedArn = parseARN(arn)
            elbv2Client = handle.client('elbv2', region_name=parsedArn['region'])
            ec2Client = handle.client('ec2', region_name=parsedArn['region'])
            # Get  the list of target groups behind this LB.
            tgs = elbv2Client.describe_target_groups(
                LoadBalancerArn=arn
            )
            for tg in tgs['TargetGroups']:
                targetHealthResponse = elbv2Client.describe_target_health(
                    TargetGroupArn=tg['TargetGroupArn']
                )
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
        else:
            elbClient = handle.client('elb', region_name=region)
            ec2Client = handle.client('ec2', region_name=region)
            res = elbClient.describe_instance_health(
                LoadBalancerName=arn
            )
            for ins in res['InstanceStates']:
                try:
                    privateIP = get_instance_private_ip(ec2Client, ins['InstanceId'])
                except Exception as e:
                    continue
                instanceInfo = {
                    'InstanceID': ins['InstanceId'],
                    'PrivateIP': privateIP
                }
                instancesInfo.append(instanceInfo)
    except Exception as e:
        print(f'Hit exception {str(e)}')
        raise e

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
