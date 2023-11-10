#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Optional, Tuple
from pydantic import BaseModel, Field
import json
from tabulate import tabulate


class InputSchema(BaseModel):
    namespace: Optional[str] = Field('', description='k8s Namespace', title='Namespace')



def k8s_get_pending_pods_printer(output):
    status, data = output

    if status:
        print("There are no pending pods.")
        return
    else:
        headers = ["Pod Name", "Namespace"]
        print(tabulate(data, headers=headers, tablefmt="grid"))


def k8s_get_pending_pods(handle, namespace:str="") -> Tuple:
    """
    k8s_get_pending_pods checks if any pod in the Kubernetes cluster is in 'Pending' status.

    :type handle: object
    :param handle: Object returned from the Task validate method

    :type namespace: string
    :param namespace: Namespace in which to look for the resources. If not provided, all namespaces are considered

    :rtype: tuple
    :return: Status,list of pending pods with their namespace
    """
    if handle.client_side_validation is not True:
        print(f"K8S Connector is invalid: {handle}")
        return False, "Invalid Handle"

    namespace_option = f"--namespace={namespace}" if namespace else "--all-namespaces"

    # Getting pods details in json format
    cmd = f"kubectl get pods -o json {namespace_option}"
    result = handle.run_native_cmd(cmd)

    if result.stderr:
        raise Exception(f"Error occurred while executing command {cmd} {result.stderr}")

    pods = json.loads(result.stdout)['items']
    pending_pods = []

    for pod in pods:
        name = pod['metadata']['name']
        status = pod['status']['phase']
        pod_namespace = pod['metadata']['namespace']

        if status == 'Pending':
            pending_pods.append([name, pod_namespace])

    if len(pending_pods) != 0:
        return (False, pending_pods)
    return (True, None)


