##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
import pprint


class InputSchema(BaseModel):
    cluster_arn: str = Field(
        title='Cluster ARN',
        description='Full ARN of the cluster.'
    )
    service_name: str = Field(
        title='Service Name',
        description='Service name to restart.'
    )
    region: str = Field(
        title='Region',
        description='AWS Region of the cloudwatch.')


def aws_ecs_service_restart_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_ecs_service_restart(handle, cluster_arn: str, service_name: str, region: str) -> bool:
    """aws_ecs_service_restart returns boolean.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type cluster_arn: string
        :param cluster_arn: Full ARN of the cluster.

        :type service_name: string
        :param service_name: ECS Service name in the specified cluster.

        :type region: string
        :param region: AWS Region of the ECS service.

        :rtype: Returns True if the service was restarted successfully and an exception if not.

    """

    # Input param validation.

    ecsClient = handle.client('ecs', region_name=region)
    ecsClient.update_service(
        cluster=cluster_arn,
        service=service_name,
        forceNewDeployment=True
    )
    try:
        waiter = ecsClient.get_waiter('services_stable')
        waiter.wait(
            cluster=cluster_arn,
            services=[service_name]
        )
    except:
        errString = f'"Failed restart service: {service_name} in cluster: {cluster_arn} after 40 checks."'
        print(errString)
        raise Exception(errString)
    return True
