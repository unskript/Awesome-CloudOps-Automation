#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    namespace: str = Field(
        title="Namespace",
        description="Namespace of the PVC."
    )
    pvc: str = Field(
        title="PVC Name",
        description="Name of the PVC."
    )

def k8s_get_pods_attached_to_pvc_printer(output):
    if output is None:
        return 
        
    print(output)



def k8s_get_pods_attached_to_pvc(handle, namespace: str, pvc: str) -> str:
    """k8s_get_pods_attached_to_pvc get pods attached to pvc

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Namespace of the PVC.

        :type pvc: str
        :param pvc: Name of the PVC.

        :rtype: string
    """
    kubectl_command = f"kubectl describe pvc {pvc} -n {namespace} | awk \'/Used By/ {{print $3}}\'"
    result = handle.run_native_cmd(kubectl_command)
    if result.stderr:
        print(
            f"Error while executing command ({kubectl_command}): {result.stderr}")
        return str()
    return result.stdout
