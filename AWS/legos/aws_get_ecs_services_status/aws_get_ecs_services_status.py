##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region of the ECS service.')


def aws_get_ecs_services_status_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_ecs_services_status(handle, region: str) -> Dict:
    """aws_get_ecs_services_status returns the status of all ECS services.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: AWS Region of the ECS service.

        :rtype: Dict with the services status status info.
    """

    healthClient = handle.client('ecs', region_name=region)

    clusters = healthClient.list_clusters()['clusterArns']
    output = {}
    for cluster in clusters:
        clusterName = cluster.split('/')[1]

        services = healthClient.list_services(cluster=clusterName)['serviceArns']
        if len(services) > 0:
            servises_status = healthClient.describe_services(cluster=cluster, services=services)
            for service in servises_status['services']:
                output[service['serviceName']] = service['status']
    return output
