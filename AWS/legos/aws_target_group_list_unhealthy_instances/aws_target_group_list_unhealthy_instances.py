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


def aws_target_group_list_unhealthy_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_target_group_list_unhealthy_instances(handle, arn: str) -> List:
    
    """aws_target_group_list_unhealthy_instances returns array of unhealthy instances

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type arn: string
        :param arn: ARN of the Target Group.

        :rtype: Returns array of unhealthy instances
    """
    # Get the region for the target group.
    parsedArn = parseARN(arn)
    elbv2Client = handle.client('elbv2', region_name=parsedArn['region'])
    try:
        targetHealthResponse = elbv2Client.describe_target_health(
            TargetGroupArn=arn
        )
    except Exception as e:
        print(f'Hit exception getting the instance list: {str(e)}')
        raise e

    instancesInfo = []
    for ins in targetHealthResponse["TargetHealthDescriptions"]:
        if ins['TargetHealth']['State'] in ['unhealthy']:
            instancesInfo.append(ins)

    return instancesInfo
