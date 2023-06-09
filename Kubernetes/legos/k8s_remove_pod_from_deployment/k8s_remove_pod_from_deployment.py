##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from kubernetes import client

class InputSchema(BaseModel):
    pod_name: str = Field(
        title="Pod Name",
        description="K8S Pod Name"
    )
    namespace: str = Field(
        title="Namespace",
        description="K8S Namespace where the POD exists"
    )

def k8s_remove_pod_from_deployment_printer(output):
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
        owner_references = pod.metadata.owner_references
        deployment_name = ''
        if isinstance(owner_references, list):
            owner_name = owner_references[0].name
            owner_kind = owner_references[0].kind 
            if owner_kind == 'Deployment':
                deployment_name = owner_name
            else:
                raise Exception(f"Unexpected owner_references kind in pod metadata {pod.metadata.owner_references} Only Deployment is supported")

        if deployment_name != '':
            deployment = apps_api.read_namespaced_deployment(
                name=deployment_name,
                namespace=namespace
                )
            deployment_labels= [key for key, value in deployment.spec.selector.match_labels.items()]

            pod_labels = [key for key,value in pod.metadata.labels.items()]

            common_labels = set(deployment_labels) & set(pod_labels)
            new_label = {}
            for label in common_labels:
                new_label[label] = pod.metadata.labels.get(label) + '-out-for-maintenance'

            pod.metadata.labels.update(new_label)
            core_api.patch_namespaced_pod(pod_name, namespace, pod)
        else:
            print(f"ERROR: Could not remove {pod_name} from its deployment in {namespace} ")
    except Exception as e:
        raise e
