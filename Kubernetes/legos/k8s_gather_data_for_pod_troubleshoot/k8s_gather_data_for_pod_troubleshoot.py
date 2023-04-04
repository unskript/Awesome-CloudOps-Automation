##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint
import json 

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

def k8s_gather_data_for_pod_troubleshoot_printer(output):
    if not output:
        return
    
    pprint.pprint(output)


def k8s_gather_data_for_pod_troubleshoot(handle, pod_name: str, namespace: str) -> str:
    """k8s_gather_data_for_pod_troubleshoot This function gathers data from the k8s namespace
       to assist in troubleshooting of a pod. The gathered data are returned in the form of a
       Dictionary with `logs`, `events` and `details` keys. 
       
       :type handle: Object
       :param handle: Object returned from task.validate(...) routine

       :type pod_name: str
       :param pod_name: Name of the K8S POD (Mandatory parameter)

       :type namespace: str 
       :param namespace: Namespace where the above K8S POD is found (Mandatory parameter)

       :rtype: Output of kubectl describe pod command
    """
    if not pod_name or not namespace:
        raise Exception("POD Name and Namespace are mandatory parameters, cannot be None")

    retval = {}
    # Get Describe POD details
    kubectl_client = f'kubectl describe pod {pod_name} -n {namespace}'
    result = handle.run_native_cmd(kubectl_client)
    if not result.stderr:
        retval['describe'] =  result.stdout 
    else:
        retval['error'] = result.stderr 
    # Get Logs for the POD 
    kubectl_client = f'kubectl logs {pod_name} -n {namespace}'
    result = handle.run_native_cmd(kubectl_client)
    if not result.stderr:
        retval['logs'] =  result.stdout 
    else:
        retval['error'] = result.stderr 
    return retval