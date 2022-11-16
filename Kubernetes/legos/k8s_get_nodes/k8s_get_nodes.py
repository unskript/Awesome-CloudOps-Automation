#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
import datetime
from typing import Tuple

import pandas as pd
from kubernetes import client
from kubernetes.client.rest import ApiException
from pydantic import BaseModel
from tabulate import tabulate


class InputSchema(BaseModel):
    pass

def k8s_get_nodes_printer(result):
    if result is None:
        return
        
    (tabular_config_map, output) = result
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
        labels = ["%s=%s" % (label, value)
                  for label, value in node.metadata.labels.items()]
        nodeStatus = (node.status.conditions)
        type = ""
        for i in nodeStatus:
            type = i.type

        name = node.metadata.name
        status = type
        age = (datetime.datetime.now() -
               node.metadata.creation_timestamp.replace(tzinfo=None)).days
        version = node.status.node_info.kubelet_version
        labels = ",".join(labels)
        tabular_config_map.append([name, status, age, version, labels])

        output.append(
            {"name": name, "status": type,
             "age": "%sd" % (datetime.datetime.now() - node.metadata.creation_timestamp.replace(tzinfo=None)).days,
             "version": version, "labels": labels})


    return (tabular_config_map, output)
