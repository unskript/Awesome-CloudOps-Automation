#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import json 
from typing import Tuple
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
    if handle.client_side_validation is not True:
        raise Exception(f"K8S Connector is invalid {handle}")

    result = []

    # Get all PVCs in the cluster
    if not namespace:
        get_pvc_command = "kubectl get pvc --all-namespaces -o=json"
        get_pod_command = "kubectl get pods --all-namespaces -o=json"
    else:
        get_pvc_command = f"kubectl get pvc -n {namespace} -o=json"
        get_pod_command = f"kubectl get pods -n {namespace} -o=json"

    try:
        # Execute the kubectl commands to get PVC and Pod information
        response_pvc = handle.run_native_cmd(get_pvc_command)
        response_pod = handle.run_native_cmd(get_pod_command)
        pvc_info = json.loads(response_pvc.stdout)
        pod_info = json.loads(response_pod.stdout)
    except Exception as e:
        raise Exception(f"Error fetching PVC or Pod information: {e.stderr}") from e

    # Extract PVC names and namespaces
    pvc_list = [(item['metadata']['name'], item['metadata']['namespace']) for item in pvc_info.get('items', [])]

    # Extract mounted PVCs from Pod information
    mounted_volumes = [(volume['persistentVolumeClaim']['claimName'], pod['metadata']['namespace']) for pod in pod_info.get('items', [])
                       for volume in pod['spec']['volumes'] if 'persistentVolumeClaim' in volume]

    # Identify unbound PVCs
    unbound_pvcs = set(pvc_list) - set(mounted_volumes)

    for pvc in unbound_pvcs:
        result.append({'name': pvc[0], 'namespace': pvc[1]})

    return (False, result) if result else (True, [])
