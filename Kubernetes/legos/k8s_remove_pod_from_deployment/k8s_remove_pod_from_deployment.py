##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint

from kubernetes import client
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    pod_name: str = Field(
        title="Pod Name",
        description="K8S Pod Name"
    )
    namespace: str = Field(
        title="Namespace",
        description="K8S Namespace where the POD exists"
    )

def k8s_remove_pod_from_deployment(output):
    if not output:
        return
    
    pprint.pprint(output)


def k8s_remove_pod_from_deployment(handle, pod_name: str, namespace: str):
    """k8s_remove_pod_from_deployment This action can be used to remove the given POD in a namespace
       from a deployment. 

       :type handle: Object
       :param handle: Object returned from task.validate(...) routine

       :type pod_name: str
       :param pod_name: Name of the K8S POD (Mandatory parameter)

       :type namespace: str 
       :param namespace: Namespace where the above K8S POD is found (Mandatory parameter)

       :rtype: None
    """
    if not pod_name or not namespace:
        raise Exception("Pod Name and Namespace are Mandatory fields")

    core_api = client.CoreV1Api(api_client=handle)

    try:
        pod = core_api.read_namespaced_pod(name=pod_name, namespace=namespace)
        pod_labels = pod.metadata.labels
        print(f"Existing Labels {pod.metadata.labels}")
        new_labels = {}
        for k,v in pod_labels.items():
            new_labels[k] = v + '-out-for-maintenance'
        
        pod.metadata.labels.update(new_labels)
        core_api.patch_namespaced_pod(pod_name, namespace, pod)
        
        newpod = core_api.read_namespaced_pod(name=pod_name, namespace=namespace)
        print(f"Updated Labels {newpod.metadata.labels}")
    except Exception as e:
        raise e
    
    return