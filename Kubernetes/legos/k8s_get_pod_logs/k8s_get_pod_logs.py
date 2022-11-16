##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from kubernetes import client
from pydantic import BaseModel, Field
import pprint

class InputSchema(BaseModel):
    namespace: str = Field(
        title='Namespace',
        description='Kubernetes namespace.')
    pod_name: str = Field(
        title='Pod',
        description='Name of the pod')


def k8s_get_pods_logs_printer(output):
    if output is None:
        return
        
    pprint.pprint(output)


def k8s_get_pod_logs(handle, namespace: str, pod_name: str) -> str:
    """k8s_get_pod_logs get pod logs

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Kubernetes namespace.

        :type pod_name: str
        :param pod_name: Name of the pod.

        :rtype: String, Output of the command in python string format or Empty String in case of Error.
    """
    coreApiClient = client.CoreV1Api(api_client=handle)

    res = coreApiClient.read_namespaced_pod_log(
        namespace=namespace, name=pod_name)
    return res
