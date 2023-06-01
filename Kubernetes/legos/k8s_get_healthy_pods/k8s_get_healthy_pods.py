##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from typing import List
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    namespace: str = Field(
        title='Namespace',
        description='Kubernetes namespace')


def k8s_get_healthy_pods_printer(data: list):
    if data is None:
        return

    print("POD List:")

    for pod in data:
        print(f"\t {pod}")

def k8s_get_healthy_pods(handle, namespace: str) -> List:
    """k8s_get_healthy_pods get healthy pods

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Kubernetes namespace.

        :rtype: List
    """
    coreApiClient = client.CoreV1Api(api_client=handle)
    try:
        coreApiClient.read_namespace_status(namespace, pretty=True)
    except ApiException as e:
        #print("Exception when calling CoreV1Api->read_namespace_status: %s\n" % e)
        raise e

    all_healthy_pods = []
    ret = coreApiClient.list_namespaced_pod(namespace=namespace)
    for i in ret.items:
        phase = i.status.phase
        if phase in ("Running", "Succeeded"):
            all_healthy_pods.append(i.metadata.name)
    return all_healthy_pods
