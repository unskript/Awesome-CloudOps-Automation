#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Optional, List
from pydantic import BaseModel
from tabulate import tabulate
import json
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    pass



def k8s_get_nodes_pressure_printer(output):
    if output is None:
        return
    headers = ['Node', 'Memory Pressure', 'Disk Pressure']
    print(tabulate(output, headers, tablefmt='pretty'))


def k8s_get_nodes_pressure(handle) -> List:
    """
    k8s_get_nodes_pressure fetches the memory and disk pressure status of each node in the cluster

    :type handle: object
    :param handle: Object returned from the Task validate method

    :rtype: List of memory and disk pressure status of each node in the cluster
    """

    if handle.client_side_validation is not True:
        print(f"K8S Connector is invalid: {handle}")
        return "Invalid Handle"

    # Getting nodes details in json format
    cmd = "kubectl get nodes -o json"
    result = handle.run_native_cmd(cmd)

    if result.stderr:
        raise ApiException(f"Error occurred while executing command {cmd} {result.stderr}")

    nodes = json.loads(result.stdout)['items']
    data = []

    for node in nodes:
        name = node['metadata']['name']
        conditions = node['status']['conditions']

        memory_pressure = next((item for item in conditions if item["type"] == "MemoryPressure"), None)
        disk_pressure = next((item for item in conditions if item["type"] == "DiskPressure"), None)

        if memory_pressure and disk_pressure:
            memory_pressure_status = memory_pressure['status']
            disk_pressure_status = disk_pressure['status']
            data.append([name, memory_pressure_status, disk_pressure_status])
    return data



