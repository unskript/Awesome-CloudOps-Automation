##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from typing import Optional, Tuple, List
import pprint

class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='AWS Region of the ECS service.')


def aws_ecs_detect_failed_deployment_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_ecs_detect_failed_deployment(handle, region: str=None) -> List:
    """aws_ecs_detect_failed_deployment returns the list .

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Optional,AWS Region of the ECS service.

        :rtype: Tuple of stopped task while deployement along with reason and status
    """
    result = []
    all_regions = [region]
    if region is None or len(region)==0:
        all_regions = aws_list_all_regions(handle=handle)
    for r in all_regions:
        try:
            healthClient = handle.client('ecs', region_name=r)
            clusters = healthClient.list_clusters()['clusterArns']
            for cluster in clusters:
                clusterName = cluster.split('/')[1]
                services = healthClient.list_services(cluster=clusterName)['serviceArns']
                if len(services) > 0:
                    servises_status = healthClient.describe_services(cluster=cluster, services=services)
                    for service in servises_status['services']:
                        deployments = service['deployments']
                        if deployments is None:
                            return (result,True)
                        for deployment in deployments:
                            if deployment['status'] == "PRIMARY":
                                primaryDeploymentID = deployment['id']
                                stoppedTasks = healthClient.list_tasks(cluster=clusterName, startedBy=primaryDeploymentID, desiredStatus="STOPPED").get('taskArns')
                                if len(stoppedTasks) == 0:
                                    continue
                                else:
                                    taskDetails = healthClient.describe_tasks(cluster=clusterName, tasks=stoppedTasks)
                                    for taskDetail in taskDetails.get('tasks'):
                                        result.append({"TaskARN":taskDetail['taskArn'], "StoppedReason":taskDetail['stoppedReason']})
        except Exception as e:
            pass
    if len(result)!=0:
        return (False,result)
    else:
        return (True, None)


