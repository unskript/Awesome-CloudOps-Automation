##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint

from kubernetes import client
from typing import Optional 
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
    deployment_label: Optional[str] = Field(
        "app",
        description="Deployment Label, default value is app",
        title="Deployment Label"
    )

def k8s_remove_pod_from_deployment(output):
    if not output:
        return

    pprint.pprint(output)


def k8s_remove_pod_from_deployment(handle, pod_name: str, namespace: str, deployment_label: str='app'):
    """k8s_remove_pod_from_deployment This action can be used to remove the given POD in a namespace
       from a deployment. 

       :type handle: Object
       :param handle: Object returned from task.validate(...) routine

       :type pod_name: str
       :param pod_name: Name of the K8S POD (Mandatory parameter)

       :type namespace: str 
       :param namespace: Namespace where the above K8S POD is found (Mandatory parameter)

       :type deployment_label: str
       :param deployment_label: Selector label if used other than app for the pod

       :rtype: None
    """
    if not pod_name or not namespace:
        raise Exception("Pod Name and Namespace are Mandatory fields")

    core_api = client.CoreV1Api(api_client=handle)
    apps_api = client.AppsV1Api(api_client=handle)

    # Labels are key-value pairs that can be attached to Kubernetes objects. 
    # Labels can be used to organize and group objects, and they can be used to 
    # select objects for operations such as deletion and updates.

    # Selectors are used to select a group of objects for an operation. Selectors can be 
    # specified using labels, and they can be used to select all objects with a given 
    # label or all objects that match a certain pattern.

    # Kubernetes deployment uses Labels and Selectors to select which pods need to be 
    # updated when a new version of a pod is deployed.

    # Here by modifying the selector label for deployment, we are making sure the pod
    # is removed from the deployment. We verify the same by listing the pod labels after
    # doing a patch operation 
    try:
        pod = core_api.read_namespaced_pod(name=pod_name, namespace=namespace)
        pod_labels = pod.metadata.labels
        new_labels = {}
        d_label = pod_labels.get(deployment_label)
        new_labels[deployment_label] = d_label + '-out-for-maintenance'

        pod.metadata.labels.update(new_labels)
        core_api.patch_namespaced_pod(pod_name, namespace, pod)

        deployment = apps_api.read_namespaced_deployment(name=d_label, namespace=namespace)
        label_selector = ','.join([f'{key}={value}' for key, value in deployment.spec.selector.match_labels.items()])
        updated_pods = core_api.list_namespaced_pod(namespace, label_selector=label_selector)
        updated_pod_names = [x.metadata.name for x in updated_pods.items]
        if pod_name not in updated_pod_names:
            print(f"Successfully Removed POD from {deployment.metadata.name} {pod_name} in {namespace} Namespace")
        else:
            print(f"ERROR: Could not remove Remove {pod_name} in {namespace} from {deployment.metadata.name}")
    except Exception as e:
        raise e

    return