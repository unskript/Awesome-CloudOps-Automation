#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#


from typing import Optional, Tuple
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException
from tabulate import tabulate

class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='k8s Namespace')


def k8s_get_pods_in_imagepullbackoff_state_printer(output):
    status, data = output

    if status:
        print("No pods are in ImagePullBackOff or ErrImagePull state.")
    else:
        headers = ["Pod Name", "Namespace", "Container Name"]
        table_data = [(entry["pod"], entry["namespace"], entry["container"]) for entry in data]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))


def k8s_get_pods_in_imagepullbackoff_state(handle, namespace: str = '') -> Tuple:
    """
    k8s_get_pods_in_imagepullbackoff_state returns the pods that have ImagePullBackOff or ErrImagePull state in their container statuses.

    :type handle: Object
    :param handle: Object returned from the task.validate(...) function

    :type namespace: str
    :param namespace: (Optional) String, K8S Namespace as python string

    :rtype: Status, List of objects of pods, namespaces, and containers in ImagePullBackOff or ErrImagePull state
    """
    result = []
    if handle.client_side_validation is not True:
        raise ApiException(f"K8S Connector is invalid {handle}")

    v1 = client.CoreV1Api(api_client=handle)

    try:
        if namespace:
            pods = v1.list_namespaced_pod(namespace).items
            if not pods:
                return (True, None)
        else:
            pods = v1.list_pod_for_all_namespaces().items
    except ApiException as e:
        raise e

    for pod in pods:
        pod_name = pod.metadata.name
        namespace = pod.metadata.namespace
        container_statuses = pod.status.container_statuses
        if container_statuses is None:
            continue
        for container_status in container_statuses:
            container_name = container_status.name
            if container_status.state and container_status.state.waiting:
                reason = container_status.state.waiting.reason
                if reason in ["ImagePullBackOff", "ErrImagePull"]:
                    result.append({"pod": pod_name, "namespace": namespace, "container": container_name})

    return (False, result) if result else (True, None)