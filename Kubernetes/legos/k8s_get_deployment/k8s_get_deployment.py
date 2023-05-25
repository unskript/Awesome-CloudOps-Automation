#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
import pprint
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException

class InputSchema(BaseModel):
    namespace: str = Field(
        title='Namespace',
        description='Kubernetes namespace.')
    deployment_name: str = Field(
        title='Deployment',
        description='Kubernetes deployment name'
    )

def k8s_get_deployment_printer(output):
    if output is None:
        return

    pprint.pprint(output)

def k8s_get_deployment(handle, namespace: str, deployment_name: str) -> str:
    """k8s_get_deployment get Kubernetes Deployment For a Pod

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Kubernetes namespace.

        :type deployment_name: str
        :param deployment_name: Kubernetes deployment name

        :rtype: string
    """
    coreApiClient = client.AppsV1Api(handle)

    try:
        field_selector = "metadata.name=" + deployment_name
        resp = coreApiClient.list_namespaced_deployment(
            namespace, pretty=True, field_selector=field_selector)

    except ApiException as e:
        resp = 'An Exception occured while executing the command' + e.reason

    return resp
