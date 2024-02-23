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
        description='K8S Namespace',
        title='K8S Namespace'
    )
    threshold: int = Field(
        25,
        description='Restart Threshold Value',
        title='Restart Threshold'
    )

def k8s_get_pods_with_high_restart_printer(output):
    if output is None:
        return

    print(output)

def k8s_get_pods_with_high_restart(handle, namespace: str = '', threshold: int = 25) -> Tuple:
    """k8s_get_pods_with_high_restart This function finds out PODS that have
       high restart count and returns them as a list of dictionaries

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :type namespace: str
       :param namespace: K8S Namespace 

       :type threshold: int 
       :param threshold: int Restart Threshold Count value

       :rtype: Tuple Result in tuple format.  
    """
    if handle.client_side_validation is not True:
        raise Exception(f"K8S Connector is invalid {handle}")

    v1 = client.CoreV1Api(api_client=handle)
    
    try:
        pods = v1.list_namespaced_pod(namespace).items if namespace else v1.list_pod_for_all_namespaces().items
        if not pods:
            return (True, None)  # No pods in the namespace
    except ApiException as e:
        raise Exception(f"Error occurred while accessing Kubernetes API: {e}")

    retval = []
    for pod in pods:
        for container_status in pod.status.container_statuses or []:
            restart_count = container_status.restart_count
            if restart_count > threshold:
                retval.append({'name': pod.metadata.name, 'namespace': pod.metadata.namespace})

    return (False, retval) if retval else (True, None)