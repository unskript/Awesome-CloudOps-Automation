##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##  @author: Yugal Pachpande, @email: yugal.pachpande@unskript.com
##
import pprint
from typing import Optional, Dict
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region of the ECS service.')
    cluster: Optional[str] = Field(
        title='Cluster Name',
        description='Cluster name that your service runs on.')
    service: str = Field(
        title='Service Name',
        description='The name of the service to update.')
    taskDefinition: str = Field(
        title='Task Definition',
        description=('The family and revision (family:revision ) or full ARN of the task '
                     'definition to run in service eg: srv-722a3657e6e3-TaskDefinition:2')
    )


def aws_ecs_update_service_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_ecs_update_service(
        handle,
        region: str,
        service: str,
        taskDefinition: str,
        cluster: str = None
        ) -> Dict:
    """aws_ecs_update_service returns the Dict .

        :type handle: object
        :param handle: Object returned from task.validate(...).
        
        :type region: string
        :param region: AWS Region of the ECS service.

        :type service: string
        :param service: ECS Service name in the specified cluster.

        :type taskDefinition: string
        :param taskDefinition: Full ARN of the task definition to run in service.

        :type cluster: string
        :param cluster: ECS Cluster name.

        :rtype: Dict of updated service.
    """
    ecs_client = handle.client('ecs', region_name=region)

    if cluster:
        response = ecs_client.update_service(
            cluster=cluster,
            service=service,
            taskDefinition=taskDefinition,
        )
    else:
        response = ecs_client.update_service(
            service=service,
            taskDefinition=taskDefinition,
        )

    return response
