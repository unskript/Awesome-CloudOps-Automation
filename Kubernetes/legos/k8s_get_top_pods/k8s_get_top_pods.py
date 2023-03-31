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

def k8s_get_top_pods_printer(output):
    if output is None:
        return 
    
    print(output)

def k8s_get_top_pods(handle) -> str:
    """k8s_get_top_pods This function returns the output of `kubectl top pods -A`

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :rtype: Tuple Result in tuple format.  
    """
    if handle.client_side_validation != True:
        raise Exception(f"K8S Connector is invalid {handle}")

    kubectl_command = "kubectl top pods --all-namespaces"
    result = handle.run_native_cmd(kubectl_command)
    if result.stderr:
        raise Exception(f"Error occurred while executing command {result.stderr}")

    return result.stdout