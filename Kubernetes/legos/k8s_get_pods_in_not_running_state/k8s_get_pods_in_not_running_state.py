#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Tuple
from pydantic import BaseModel, Field
import json


class InputSchema(BaseModel):
    namespace: str = Field(
        '',
        description='K8S Namespace',
        title='K8S Namespace'
    )

def k8s_get_pods_in_not_running_state_printer(output):
    if output is None:
        return

    print(output)


def k8s_get_pods_in_not_running_state(handle, namespace: str = '') -> Tuple:
    """k8s_get_pods_in_not_running_state this check function checks for pods not in "Running" state and status.phase is not "Succeeded" 
       and returns the output of list of pods. It does not consider "Completed" status as an errored state.

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :rtype: Tuple Result in tuple format.  
    """
    if handle.client_side_validation is not True:
        raise Exception(f"K8S Connector is invalid {handle}")

    cmd_base = "kubectl get pods"
    ns_arg = f"-n {namespace}" if namespace else "--all-namespaces"
    field_selector = "--field-selector=status.phase!=Running,status.phase!=Succeeded"
    output_format = "-o json"

    kubectl_command = f"{cmd_base} {ns_arg} {field_selector} {output_format}"
    result = handle.run_native_cmd(kubectl_command)

    if result.stderr:
        raise Exception(f"Error occurred while executing command {kubectl_command}: {result.stderr}")
    
    failed_pods = []
    if result.stdout:
        pods = json.loads(result.stdout).get("items", [])
        if pods:
            failed_pods = [{'name': pod['metadata']['name'], 
                            'namespace': pod['metadata']['namespace'], 
                            'status': pod['status']['phase']} for pod in pods]
            return (False, failed_pods)

    return (True, None)
