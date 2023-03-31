#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Tuple
from kubernetes import client
from kubernetes.client.rest import ApiException
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    pass

def k8s_get_unbound_pvcs_printer(output):
    if output is None:
        return 
    
    print(output)

def k8s_get_unbound_pvcs(handle) -> Tuple:
    """k8s_get_unbound_pvcs This function all unbound PVCS and returns them back

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :rtype: Tuple Result in tuple format.  
    """
    if handle.client_side_validation != True:
        raise Exception(f"K8S Connector is invalid {handle}")

    v1 = client.CoreV1Api(api_client=handle)

    # Get all PVCs in the cluster
    pvc_list = v1.list_persistent_volume_claim_for_all_namespaces().items
    retval = []
    # Iterate through each PVC and check its status
    for pvc in pvc_list:
        # Check if the PVC is bound to a volume
        if pvc.status.phase != "Bound":
            retval.append(pvc)

    if retval:
        return (False, retval)
    
    return (True, [])