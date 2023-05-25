##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from tabulate import tabulate
from kubernetes import client

pp = pprint.PrettyPrinter(indent=2)


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='all',
        title='Namespace',
        description='k8s namespace')


def k8s_get_all_pods_printer(output):
    (healthy_pods, unhealthy_pods, data) = output

    if len(healthy_pods) > 0:
        print("\n Healthy PODS \n")
        print(tabulate(healthy_pods, headers=[
            "NAME", "READY", "STATUS", "RESTARTS", "Age"]))

    if len(unhealthy_pods) > 0:
        print("\n UnHealthy PODS \n")
        print(tabulate(unhealthy_pods, headers=[
            "NAME", "READY", "STATUS", "RESTARTS", "Age"]))


def k8s_get_all_pods(handle, namespace: str = "all") -> Tuple:

    """k8s_get_all_pods get all pods

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: k8s namespace.

        :rtype: Tuple
    """
    coreApiClient = client.CoreV1Api(api_client=handle)

    healthy_pods = []
    unhealthy_pods = []
    data = coreApiClient.list_namespaced_pod(namespace=namespace, pretty=True)
    for i in data.items:
        for container_status in i.status.container_statuses:
            if container_status.ready is False:
                waiting_state = container_status.state.waiting
                status = waiting_state.reason
                unhealthy_pods.append([i.metadata.name,
                                       str(0) + "/" + str(len(i.status.container_statuses)),
                                       status,
                                       container_status.restart_count,
                                       i.status.start_time
                                       ])
            else:
                healthy_pods.append([
                    i.metadata.name,
                    str(len(i.status.container_statuses)) + "/" + str(len(i.status.container_statuses)),
                    i.status.phase,
                    container_status.restart_count,
                    i.status.start_time
                    ])


    return (healthy_pods, unhealthy_pods, data)
