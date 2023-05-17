##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from kubernetes import client

class InputSchema(BaseModel):
    namespace: str = Field(
        title='Namespace',
        description='Kubernetes namespace')
    pod: str = Field(
        title="Pod",
        description='Kubernetes Pod Name. eg ngix-server')


def k8s_get_pod_config_printer(output):
    if output is None:
        return

    pprint.pprint(output)

def k8s_get_pod_config(handle, namespace: str, pod: str) -> str:
    """k8s_get_pod_config get pod config

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Kubernetes namespace.

        :type pod: str
        :param pod: Kubernetes Pod Name.

        :rtype: string
    """
    coreApiClient = client.AppsV1Api(api_client=handle)

    field_selector = "metadata.name=" + pod
    res = coreApiClient.list_namespaced_deployment(
        namespace=namespace, pretty=True, field_selector=field_selector)
    return res
