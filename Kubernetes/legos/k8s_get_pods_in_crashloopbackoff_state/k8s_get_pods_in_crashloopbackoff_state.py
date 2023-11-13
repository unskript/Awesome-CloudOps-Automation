#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

import json 

from typing import Optional, Tuple
from pydantic import BaseModel, Field
from tabulate import tabulate


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='k8s Namespace')


def k8s_get_pods_in_crashloopbackoff_state_printer(output):
    status, data = output

    if status:
        print("No pods are in CrashLoopBackOff state.")
    else:
        headers = ["Pod Name", "Namespace", "Container Name"]
        table_data = [(entry["pod"], entry["namespace"], entry["container"]) for entry in data]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

def k8s_get_pods_in_crashloopbackoff_state(handle, namespace: str = '') -> Tuple:
    """
    k8s_get_pods_in_crashloopbackoff_state returns the pods that have CrashLoopBackOff state in their container statuses.

    :type namespace: str
    :param namespace: (Optional) String, K8S Namespace as python string

    :rtype: Status, List of objects of pods, namespaces, and containers that are in CrashLoopBackOff state
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

    for pod_info in pods_info['items']:
        pod_name = pod_info['metadata']['name']
        namespace = pod_info['metadata'].get('namespace', '')

        container_statuses = pod_info['status'].get('containerStatuses', [])
        for container_status in container_statuses:
            container_name = container_status.get('name', '')
            if container_status.get('state', {}).get('waiting', {}).get('reason') == "CrashLoopBackOff":
                result.append({"pod": pod_name, "namespace": namespace, "container": container_name})

    return (False, result) if result else (True, None)
