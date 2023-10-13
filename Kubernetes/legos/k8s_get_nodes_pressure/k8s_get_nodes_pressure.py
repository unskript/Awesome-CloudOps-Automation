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

    status, data = output

    if status:
        print("No nodes have memory or disk pressure issues.")
        return

    headers = ['Node', 'Type', 'Status']
    formatted_data = [[item['node'], item['type'], item['status']] for item in data]
    print(tabulate(formatted_data, headers=headers, tablefmt='pretty'))



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
    pressure_nodes = []

    for node in nodes:
        name = node['metadata']['name']
        conditions = node['status']['conditions']

        memory_pressure = next((item for item in conditions if item["type"] == "MemoryPressure"), None)
        disk_pressure = next((item for item in conditions if item["type"] == "DiskPressure"), None)

        # Check for pressure conditions being False
        if memory_pressure and memory_pressure['status'] != "False":
            pressure_nodes.append({"node": name, "type": "MemoryPressure", "status": "False"})

        if disk_pressure and disk_pressure['status'] != "False":
            pressure_nodes.append({"node": name, "type": "DiskPressure", "status": "False"})

    if len(pressure_nodes) != 0:
        return (False, pressure_nodes)
    return (True, None)



