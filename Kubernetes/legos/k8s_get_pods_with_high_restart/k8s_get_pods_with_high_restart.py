#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Tuple
from pydantic import BaseModel, Field
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    namespace: str = Field(
        '',
        description='K8S Namespace',
        title='K8S Namespace'
    )
    threshold: int = Field(
        10,
        description='Restart Threshold Value',
        title='Restart Threshold'
    )

def k8s_get_pods_with_high_restart_printer(output):
    if output is None:
        return

    print(output)

def k8s_get_pods_with_high_restart(handle, namespace: str = '', threshold: int = 10) -> Tuple:
    """k8s_get_pods_with_high_restart This function finds out PODS that have
       high restart count and returns them as a list of dictionaries

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :type namespace: str
       :param namespace: K8S Namespace 

       :type threshold: int 
       :param threshold: int Restart Threshold Count value

       :rtype: Tuple Result in tuple format.  
    """
    if handle.client_side_validation is not True:
        raise ApiException(f"K8S Connector is invalid {handle}")

    if not namespace :
        kubectl_command = "kubectl get pods --all-namespaces --no-headers  | " + \
            f"awk '$5 > {threshold} " + " {print $0}' | awk '{print $1,$2}'"
    else:
        kubectl_command = f"kubectl get pods -n {namespace}" + " --no-headers  | " + \
            f"awk '$4 > {threshold} " + " {print $0}' | awk '{print $1,$2}'"

    result = handle.run_native_cmd(kubectl_command)
    if result.stderr:
        raise ApiException(f"Error occurred while executing command {result.stderr}")
    retval = []
    if result.stdout:
        for line in result.stdout.split('\n'):
            if not line:
                continue
            n,p = line.split(' ')
            if not namespace:
                retval.append({'name': p, 'namespace': n})
            else:
                retval.append({'name': n, 'namespace': namespace})
    if retval:
        return (False, retval)

    return (True, [])
