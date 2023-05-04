##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    cluster_name: str = Field(
        title="Cluster name",
        description="ECS Cluster name"
    )
    service_name: str = Field(
        title="Service name",
        description="ECS Service name in the specified cluster."
    )
    region: str = Field(
        title='Region',
        description='AWS Region of the ECS service.')


def aws_ecs_detect_failed_deployment_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_ecs_detect_failed_deployment(
    handle,
    cluster_name: str,
    service_name: str,
    region: str
    ) -> List:
    """aws_ecs_detect_failed_deployment returns the list .

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type cluster_name: string
        :param cluster_name: ECS Cluster name.

        :type service_name: string
        :param service_name: ECS Service name in the specified cluster.

        :type region: string
        :param region: AWS Region of the ECS service.

        :rtype: List of stopped task while deployement along with reason.
    """
    ecsClient = handle.client('ecs', region_name=region)
    try:
        serviceStatus = ecsClient.describe_services(cluster=cluster_name, services=[service_name])
    except Exception as e:
        print(f'Failed to get service status for {service_name}, cluster {cluster_name}, {e}')
        return [f'Failed to get service status for {service_name}, cluster {cluster_name}, {e}']
    # When the deployment is in progress, there will be 2 deployment entries, one PRIMARY and
    # one ACTIVE. PRIMARY will eventually replace ACTIVE, if its successful.
    deployments = serviceStatus.get('services')[0].get('deployments')
    if deployments is None:
        print("Empty deployment")
        return ["Empty deployment"]

    deploymentInProgress = False
    for deployment in deployments:
        if deployment['status'] == "PRIMARY":
            primaryDeploymentID = deployment['id']
        else:
            deploymentInProgress = True

    if deploymentInProgress is False:
        print("No deployment in progress")
        return ["No deployment in progress"]

    # Check if there are any stopped tasks because of this deployment
    stoppedTasks = ecsClient.list_tasks(
        cluster=cluster_name,
        startedBy=primaryDeploymentID,
        desiredStatus="STOPPED"
        ).get('taskArns')
    if len(stoppedTasks) == 0:
        print(f"No stopped tasks associated with the deploymentID {primaryDeploymentID}, "
              f"service {service_name}, cluster {cluster_name}")
        return [(f'No stopped tasks associated with the deploymentID {primaryDeploymentID}, '
                f'service {service_name}, cluster {cluster_name}')]

    # Get the reason for the stopped tasks
    taskDetails = ecsClient.describe_tasks(cluster=cluster_name, tasks=stoppedTasks)
    output = []
    for taskDetail in taskDetails.get('tasks'):
        output.append({
            "TaskARN":taskDetail['taskArn'],
            "StoppedReason":taskDetail['stoppedReason']
            })
    return output
