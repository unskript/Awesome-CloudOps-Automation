#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Tuple
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    namespace: str = Field(
        '',
        description="K8S Namespace",
        title="K8S Namespace"
    )

def k8s_get_failed_deployments_printer(output):
    if output is None:
        return

    print(output)


def k8s_get_failed_deployments(handle, namespace: str = '') -> Tuple:
    """k8s_get_failed_deployments Returns the list of all failed deployments across all namespaces

    :type handle: Object
    :param handle: Object returned from task.validate(...) function

    :rtype: Tuple of the result
    """
    if handle.client_side_validation is not True:
        raise ApiException(f"K8S Connector is invalid {handle}")

    apps_client = client.AppsV1Api(api_client=handle)
    if not namespace:
        deployments = apps_client.list_deployment_for_all_namespaces().items 
    else:
        deployments = apps_client.list_namespaced_deployment(namespace).items

    retval = []
    for deployment in deployments:
        cond_dict = deployment.status.conditions[0].to_dict()
        if cond_dict.get('status') == 'False':
            retval.append({
                'name': deployment.metadata.name,
                'namespace': deployment.metadata.namespace
                })

    if retval:
        return (False, retval)

    return (True, [])
