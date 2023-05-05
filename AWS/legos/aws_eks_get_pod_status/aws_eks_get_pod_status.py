# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
# @author: Yugal Pachpande, @email: yugal.pachpande@unskript.com
##

import pprint
from typing import Optional, Dict
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_get_handle.aws_get_handle import Session
from kubernetes import client


class InputSchema(BaseModel):
    clusterName: str = Field(
        title='Cluster Name',
        description='Name of cluster')
    namespace: Optional[str] = Field(
        title='Cluster Namespace',
        description='Cluster Namespace')
    pod_name: str = Field(
        title='Pod Name',
        description='Name of the pod.')
    region: str = Field(
        title='Region',
        description='AWS Region of the cluster')


def aws_eks_get_pod_status_printer(output):
    if output is None:
        return
    print("\n")
    pprint.pprint(output)


def aws_eks_get_pod_status(
        handle: Session,
        clusterName: str,
        pod_name: str,
        region: str,
        namespace: str = None
        ) -> Dict:
    """aws_eks_get_pod_status returns Dict.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type clusterName: string
        :param clusterName: Cluster name.

        :type pod_name: string
        :param pod_name: Name of the pod.

        :type namespace: string
        :param namespace: Cluster Namespace.

        :type region: string
        :param region: AWS Region of the EKS cluster.

        :rtype: Dict of pods details with status.
    """
    k8shandle = handle.unskript_get_eks_handle(clusterName, region)
    coreApiClient = client.CoreV1Api(api_client=k8shandle)
    status = coreApiClient.read_namespaced_pod_status(
        namespace=namespace, name=pod_name)

    res = {}

    ready_containers_number = 0
    containers_number = 0
    restarts_number = 0

    for container in status.status.container_statuses:
        if container.ready:
            ready_containers_number += 1
        if container.restart_count:
            restarts_number = restarts_number + container.restart_count
        containers_number += 1
    res["NAME"] = pod_name
    res['READY'] = f"Ready {ready_containers_number}/{containers_number}"
    res['STATUS'] = status.status.phase
    res['RESTARTS'] = restarts_number
    res['START_TIME'] = status.status.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    return res
