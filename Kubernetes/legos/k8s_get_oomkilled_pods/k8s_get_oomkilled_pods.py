#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import json
import pprint
from typing import Tuple, Optional
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        '',
        description='Kubernetes Namespace Where the Service exists',
        title='K8S Namespace',
    )



def k8s_get_oomkilled_pods_printer(output):
    if output is None:
        return
    pprint.pprint(output)
    

def k8s_get_oomkilled_pods(handle, namespace: str = "") -> Tuple:
    """
    k8s_get_oomkilled_pods This function returns the pods that have OOMKilled event in the container last states

    :type handle: object
    :param handle: Object as returned from the task.validate(...)

    :type namespace: str
    :param namespace: (Optional) String, K8S Namespace as python string

    :rtype: Status, List of objects of pods, namespaces, and containers that are in OOMKilled state
    """
    result = []

    # If namespace is provided, get pods from the specified namespace
    if namespace:
        get_pods_command = f"kubectl get pods -n {namespace} -o=json"
    # If namespace is not provided, get pods from all namespaces
    else:
        get_pods_command = "kubectl get pods --all-namespaces -o=json"

    try:
        # Execute the kubectl command to get pod information
        response = handle.run_native_cmd(get_pods_command)
        pods_info = json.loads(response.stdout)
    except Exception as e:
        raise Exception(f"Error fetching pod information: {e.stderr}") from e

    for pod_info in pods_info.get('items', []):
        pod_name = pod_info['metadata']['name']
        namespace = pod_info['metadata'].get('namespace', '')

        # Ensure container_statuses is not None before iterating
        container_statuses = pod_info['status'].get('containerStatuses', [])
        if not container_statuses:
            continue

        # Check each pod for OOMKilled state
        for container_status in container_statuses:
            container_name = container_status['name']
            last_state = container_status.get('lastState', {}).get('terminated', {})
            if last_state and last_state.get('reason') == "OOMKilled":
                result.append({"pod": pod_name, "namespace": namespace, "container": container_name})

    return (False, result) if result else (True, None)