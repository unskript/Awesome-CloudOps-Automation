#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Tuple
from pydantic import BaseModel
from kubernetes.client.rest import ApiException
import json


class InputSchema(BaseModel):
    pass



def k8s_get_offline_nodes_printer(output):
    if output is None:
        return
    print(output)


def k8s_get_offline_nodes(handle) -> Tuple:
    """
    k8s_get_offline_nodes checks if any node in the Kubernetes cluster is offline.

    :type handle: object
    :param handle: Object returned from the Task validate method

    :rtype: tuple
    :return: Status, List of offline nodes
    """

    if handle.client_side_validation is not True:
        print(f"K8S Connector is invalid: {handle}")
        return (False, ["Invalid Handle"])

    # Getting nodes details in json format
    cmd = "kubectl get nodes -o json"
    result = handle.run_native_cmd(cmd)

    if result.stderr:
        raise ApiException(f"Error occurred while executing command {cmd} {result.stderr}")

    nodes = json.loads(result.stdout)['items']
    offline_nodes = []

    for node in nodes:
        name = node['metadata']['name']
        conditions = node['status']['conditions']

        node_ready = next((item for item in conditions if item["type"] == "Ready"), None)

        if node_ready and node_ready['status'] == "False":
            offline_nodes.append(name)

    if len(offline_nodes) != 0:
        return (False, offline_nodes)
    return (True, None)




