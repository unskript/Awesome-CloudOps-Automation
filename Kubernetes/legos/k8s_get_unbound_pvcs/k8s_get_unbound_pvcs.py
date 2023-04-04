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
    matched_volume = {}
    list_all_volumes = {}
    # Iterate through each PVC and check its status
    for pvc in pvc_list:
        # Check if the PVC is bound to a volume
        for pod in pod_list:
            found = False
            for volume in pod.spec.volumes:
                if volume.persistent_volume_claim != None:
                    if volume.persistent_volume_claim.claim_name == pvc.metadata.name:
                        found = True
                        matched_volume[pvc.metadata.name] = pvc.metadata.namespace
                        list_all_volumes[pvc.metadata.name] = pvc.metadata.namespace
                        break
                    else:
                        list_all_volumes[pvc.metadata.name] = pvc.metadata.namespace
    
    if len(matched_volume) != len(list_all_volumes):
       for k,v in list_all_volumes.items():
           if k not in matched_volume.keys():
               retval.append({'name': k, 'namespace': v})

    if retval:
        return (False, retval)
    
    return (True, [])