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


def k8s_get_pods_in_crashloopbackoff_state_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def k8s_get_pods_in_crashloopbackoff_state(handle, namespace: str = '') -> Tuple:
    """
    k8s_get_pods_in_crashloopbackoff_state returns the pods that have CrashLoopBackOff state in their container statuses.

    :type handle: Object
    :param handle: Object returned from the task.validate(...) function

    :type namespace: str
    :param namespace: (Optional) String, K8S Namespace as python string

    :rtype: Status, List of objects of pods, namespaces, and containers that are in CrashLoopBackOff state
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
        # Check each pod for CrashLoopBackOff state
        for container_status in pod.status.container_statuses:
            container_name = container_status.name
            if container_status.state and container_status.state.waiting and container_status.state.waiting.reason == "CrashLoopBackOff":
                result.append({"pod": pod_name, "namespace": namespace, "container": container_name})

    return (False, result) if result else (True, None)