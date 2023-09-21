#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='k8s Namespace')


def k8s_get_pods_in_terminating_state_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def k8s_get_pods_in_terminating_state(handle, namespace: str = '') -> Tuple:
    """
    This function returns the pods that are in the Terminating state.

    :type handle: Object
    :param handle: Object returned from the task.validate(...) function

    :type namespace: str
    :param namespace: (Optional) String, K8S Namespace as python string

    :rtype: Status, List of objects of pods, namespaces, and containers that are in Terminating state
    """
    result = []
    if handle.client_side_validation is not True:
        raise ApiException(f"K8S Connector is invalid {handle}")

    v1 = client.CoreV1Api(api_client=handle)

    # Check whether a namespace is provided, if not fetch all namespaces
    try:
        if namespace:
            pods = v1.list_namespaced_pod(namespace).items
        else:
            pods = v1.list_pod_for_all_namespaces().items
    except ApiException as e:
        raise e

    for pod in pods:
        pod_name = pod.metadata.name
        namespace = pod.metadata.namespace
        # Check each pod for Terminating state
        if pod.metadata.deletion_timestamp is not None:
            result.append({"pod": pod_name, "namespace": namespace})

    return (False, result) if result else (True, None)
