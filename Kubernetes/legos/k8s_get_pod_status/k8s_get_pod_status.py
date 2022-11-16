##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Dict
from kubernetes import client
from pydantic import BaseModel, Field
from tabulate import tabulate


class InputSchema(BaseModel):
    namespace: str = Field(
        title='Namespace',
        description='Kubernetes namespace')
    pod_name: str = Field(
        title='Pod',
        description='Name of the pod')


def k8s_get_pod_status_printer(data):
    if data is None:
        return 
    pprint.pprint(data)

def k8s_get_pod_status(handle, namespace: str, pod_name: str) -> Dict:
    """k8s_get_pod_status get pod status

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Kubernetes namespace.

        :type pod_name: str
        :param pod_name: Name of the pod.

        :rtype: Dict
    """
    coreApiClient = client.CoreV1Api(api_client=handle)

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
    res['READY'] = "Ready {}/{}".format(ready_containers_number,
                                        containers_number)
    res['STATUS'] = status.status.phase
    res['RESTARTS'] = restarts_number
    res['START_TIME'] = status.status.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    return res
