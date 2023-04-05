#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Tuple
from kubernetes import client
from kubernetes.client.rest import ApiException
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    namespace: str = Field(
        '',
        description='K8S Namespace',
        title='K8S Namespace'
    )

def k8s_get_pods_in_not_running_state(output):
    if output is None:
        return 
    
    print(output)


def k8s_get_pods_in_not_running_state(handle, namespace: str = '') -> Tuple:
    """k8s_get_pods_in_not_running_state This check function uses the handle's native command
       method to execute a pre-defined kubectl command and returns the output of list of pods
       not in running state.

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :rtype: Tuple Result in tuple format.  
    """
    if handle.client_side_validation != True:
        raise Exception(f"K8S Connector is invalid {handle}")

    if not namespace:
        kubectl_command = "kubectl get pods --all-namespaces --field-selector=status.phase!=Running -o jsonpath=\"{.items[*]['metadata.name', 'metadata.namespace']}\""
    else:
        kubectl_command = f"kubectl get pods -n {namespace}" +  " --field-selector=status.phase!=Running -o jsonpath=\"{.items[*]['metadata.name', 'metadata.namespace']}\""
    result = handle.run_native_cmd(kubectl_command)
    if result.stderr:
        raise Exception(f"Error occurred while executing command {kubectl_command} {result.stderr}")
    
    if result.stdout:
        return (False, [{'name': result.stdout.split()[0], 'namespace': result.stdout.split()[-1]}])
    
    return (True, [])