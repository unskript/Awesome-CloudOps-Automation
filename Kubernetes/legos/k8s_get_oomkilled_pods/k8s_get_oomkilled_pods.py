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
       :param namespace: String, K8S Namespace as python string

       :rtype: Tuple Result in tuple format.
    """
    result = []
    if handle.client_side_validation is not True:
        raise ApiException(f"K8S Connector is invalid {handle}")

    v1 = client.CoreV1Api(api_client=handle)
    pods = v1.list_pod_for_all_namespaces().items
    pods_to_check = pods
    if namespace != "":
        for p in pods:
            if p.metadata.namespace == namespace:
                pods_to_check = p
                break
    for pod in pods_to_check:
        pod_name = pod.metadata.name
        namespace = pod.metadata.namespace

        for container_status in pod.status.container_statuses:
            container_name = container_status.name
            last_state = container_status.last_state
            if last_state and last_state.terminated and last_state.terminated.reason == "OOMKilled":
                result.append({"pod": pod_name, "namespace": namespace, "container": container_name})
    if result:
        return (False, result)
    return(True, None)


