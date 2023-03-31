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

def k8s_get_pods_with_high_restart_printer(output):
    if output is None:
        return 
    
    print(output)

def k8s_get_pods_with_high_restart(handle) -> Tuple:
    """k8s_get_pods_with_high_restart This function finds out PODS that have
       high restart count and returns them as a list of dictionaries

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :rtype: Tuple Result in tuple format.  
    """
    if handle.client_side_validation != True:
        raise Exception(f"K8S Connector is invalid {handle}")

    kubectl_command = "kubectl get pods --all-namespaces --no-headers  | awk '$5 > 10 {print $0}'  | awk '{print $1,$2}'"
    result = handle.run_native_cmd(kubectl_command)
    if result.stderr:
        raise Exception(f"Error occurred while executing command {result.stderr}")
    retval = {}
    if result.stdout:
        for line in result.stdout.split('\n'):
            if not line:
                continue
            n,p = line.split(' ')
            if n in retval.keys():
                retval[n].append(p)
            else:
                retval[n] = [p]
    if retval:
        return (False, retval)
    
    return (True, [])