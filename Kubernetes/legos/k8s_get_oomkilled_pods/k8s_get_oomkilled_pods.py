#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import pprint
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        '',
        description='Kubernetes Namespace Where the Service exists',
        title='K8S Namespace',
    )



def k8s_get_oomkilled_pods_printer(output):
    if output is None:
        return
    pprint.pprint(output)
    

def k8s_get_oomkilled_pods(handle, namespace: str = "") -> Tuple:
    """k8s_get_oomkilled_pods This function returns the pods that have OOMKilled event in the container last states

    :type handle: Object
    :param handle: Object returned from the task.validate(...) function

    :type namespace: str
    :param namespace: (Optional)String, K8S Namespace as python string

    :rtype: Status, List of objects of pods, namespaces, and containers that are in OOMKilled state
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
    # Check each pod for OOMKilled state
        for container_status in pod.status.container_statuses:
            container_name = container_status.name
            last_state = container_status.last_state
            if last_state and last_state.terminated and last_state.terminated.reason == "OOMKilled":
                result.append({"pod": pod_name, "namespace": namespace, "container": container_name})

    return (False, result) if result else (True, None)



