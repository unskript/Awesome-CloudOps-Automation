#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

import json 
import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field



class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='k8s Namespace')


def k8s_get_pods_in_terminating_state_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def k8s_get_pods_in_terminating_state(handle, namespace: str = '') -> Tuple:
    """
    This function returns the pods that are in the Terminating state.

    :type handle: object
    :param handle: Object returned from task.validate(...) method

    :type namespace: str
    :param namespace: (Optional) String, K8S Namespace as python string

    :rtype: Status, List of objects of pods, namespaces, and containers that are in Terminating state
    """
    result = []

    # If namespace is provided, get pods from the specified namespace
    if namespace:
        get_pods_command = f"kubectl get pods -n {namespace} --field-selector=status.phase=Terminating -o=json"
    # If namespace is not provided, get pods from all namespaces
    else:
        get_pods_command = "kubectl get pods --all-namespaces --field-selector=status.phase=Terminating -o=json"

    try:
        # Execute the kubectl command to get pod information
        response = handle.run_native_cmd(get_pods_command)
        pods_info = json.loads(response.stdout)
    except Exception as e:
        raise Exception(f"Error fetching pod information: {e.stderr}") from e

    for pod_info in pods_info.get('items', []):
        pod_name = pod_info['metadata']['name']
        namespace = pod_info['metadata'].get('namespace', '')
        result.append({"pod": pod_name, "namespace": namespace})

    return (False, result) if result else (True, None)

