#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
import datetime
from typing import Tuple
from pydantic import BaseModel
from tabulate import tabulate
from kubernetes import client
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    pass

def k8s_get_nodes_printer(result):
    if result is None:
        return

    tabular_config_map = result[0]
    print("\n")
    print(tabulate(tabular_config_map, tablefmt="github",
                headers=['name', 'status', 'age', 'version', 'labels']))

def k8s_get_nodes(handle) -> Tuple:
    """k8s_get_nodes get nodes

        :rtype: Tuple
    """
    coreApiClient = client.CoreV1Api(api_client=handle)

    try:
        resp = coreApiClient.list_node(pretty=True)

    except ApiException as e:
        resp = 'An Exception occured while executing the command' + e.reason
        raise e

    output = []
    tabular_config_map = []
    for node in resp.items:
        print(node.metadata.labels)
        labels = [f"{label}={value}"
                  for label, value in node.metadata.labels.items()]
        nodeStatus = node.status.conditions
        types = ""
        for i in nodeStatus:
            types = i.type

        name = node.metadata.name
        status = types
        age = (datetime.datetime.now() -
               node.metadata.creation_timestamp.replace(tzinfo=None)).days
        version = node.status.node_info.kubelet_version
        labels = ",".join(labels)
        tabular_config_map.append([name, status, age, version, labels])

        output.append({
            "name": name,
            "status": types,
            "age": f"{(datetime.datetime.now() - node.metadata.creation_timestamp.replace(tzinfo=None)).days}d",
            "version": version, "labels": labels})

    return (tabular_config_map, output)
