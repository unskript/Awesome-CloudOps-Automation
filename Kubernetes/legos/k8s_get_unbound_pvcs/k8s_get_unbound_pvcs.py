#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Tuple
from kubernetes import client
from kubernetes.client.rest import ApiException
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    namespace: str = Field (
        '',
        description='K8S Namespace',
        title="K8S Namespace"
    )

def k8s_get_unbound_pvcs_printer(output):
    if output is None:
        return 
    
    print(output)

def k8s_get_unbound_pvcs(handle, namespace:str = '') -> Tuple:
    """k8s_get_unbound_pvcs This function all unbound PVCS and returns them back

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :type namespace: str
       :param namespace: Kubernetes Namespace 

       :rtype: Tuple Result in tuple format.  
    """
    if handle.client_side_validation != True:
        raise Exception(f"K8S Connector is invalid {handle}")

    v1 = client.CoreV1Api(api_client=handle)

    # Get all PVCs in the cluster
    if not namespace:
        pvc_list = v1.list_persistent_volume_claim_for_all_namespaces().items
        pod_list = v1.list_pod_for_all_namespaces().items
    else:
        pvc_list = v1.list_namespaced_persistent_volume_claim(namespace).items
        pod_list = v1.list_namespaced_pod(namespace).items

    retval = []
    mounted_volume = []
    list_all_volumes = []
    # Iterate through each PVC 
    for pvc in pvc_list:
        list_all_volumes.append([pvc.metadata.name, pvc.metadata.namespace])
    
    for pod in pod_list:
        for volume in pod.spec.volumes:
                if volume.persistent_volume_claim != None:
                    mounted_volume.append([volume.persistent_volume_claim.claim_name,  pod.metadata.namespace])
    
    if len(mounted_volume) != len(list_all_volumes):
        unmounted_volumes = set([x[0] for x in list_all_volumes]) - set([x[0] for x in mounted_volume])
        for um in unmounted_volumes:
            n = [x for x in list_all_volumes if x[0] == um][0]
            unmounted_pvc_name = n[0]
            unmounted_pvc_namespace = n[1]
            retval.append({'name': unmounted_pvc_name, 'namespace': unmounted_pvc_namespace})

    if retval:
        return (False, retval)
    
    return (True, [])