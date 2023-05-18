#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    namespace: str = Field(
        title='Namespace',
        description='Kubernetes namespace')

def k8s_get_services_printer(output):
    if output is None:
        return

    print(output)


def k8s_get_services(handle, namespace: str) -> str:
    """k8s_get_services get services

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Kubernetes namespace.

        :rtype: string
    """
    coreApiClient = client.CoreV1Api(api_client=handle)

    try:
        resp = coreApiClient.list_namespaced_service(namespace)

    except ApiException as e:
        resp = 'An Exception occured while executing the command' + e.reason

    return resp
