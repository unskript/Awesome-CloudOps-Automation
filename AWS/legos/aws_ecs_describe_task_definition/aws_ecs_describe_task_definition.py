##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##  @author: Yugal Pachpande, @email: yugal.pachpande@unskript.com
##
from pydantic import BaseModel, Field
from typing import Dict
import pprint


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region of the ECS service.')
    taskDefinition: str = Field(
        title='TaskDefinition',
        description='The family and revision (family:revision ) or full ARN of the task definition to run in service eg: srv-722a3657e6e3-TaskDefinition:2'
    )



def aws_ecs_describe_task_definition_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_ecs_describe_task_definition(handle, region: str, taskDefinition: str) -> Dict:
    """aws_ecs_describe_task_definition returns Dict .

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type taskDefinition: string
        :param taskDefinition: Full ARN of the task definition to run in service.

        :type region: string
        :param region: AWS Region of the ECS service.

        :return: Dict resp of task defination.

    """
    ecs_client = handle.client('ecs', region_name=region)
    try:
        data = ecs_client.describe_task_definition(taskDefinition=taskDefinition)
    except Exception as e:
        errString = f'"Error to describe task definition {str(e)}"'
        print(errString)
        raise Exception(errString)
    return data
