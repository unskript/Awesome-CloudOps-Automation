#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import List
from tabulate import tabulate
import json
from kubernetes.client.rest import ApiException
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def k8s_get_node_status_and_resource_utilization_printer(output):
    if not output:
        print("No Data to Display")
    else:
        headers = ['Node Name', 'Status', 'CPU Usage (%)', 'Memory Usage (%)']
        print(tabulate(output, headers, tablefmt='pretty'))


def k8s_get_node_status_and_resource_utilization(handle) -> List:
    if handle.client_side_validation is not True:
        print(f"K8S Connector is invalid: {handle}")
        return []

    # Command to fetch node resource utilization
    node_utilization_cmd = "kubectl top nodes --no-headers"
    node_utilization = handle.run_native_cmd(node_utilization_cmd)
    if node_utilization.stderr:
        raise ApiException(f"Error occurred while executing command {node_utilization_cmd} {node_utilization.stderr}")

    utilization_lines = node_utilization.stdout.split('\n')

    # Command to fetch node status
    node_status_cmd = "kubectl get nodes -o json"
    node_status = handle.run_native_cmd(node_status_cmd)
    if node_status.stderr:
        raise ApiException(f"Error occurred while executing command {node_status_cmd} {node_status.stderr}")

    nodes_info = json.loads(node_status.stdout)

    data = []
    for item, utilization_line in zip(nodes_info['items'], utilization_lines):
        node_name = item['metadata']['name']
        node_status = item['status']['conditions'][-1]['type']
        utilization_parts = utilization_line.split()
        cpu_usage_percent = utilization_parts[2].rstrip('%')
        memory_usage_percent = utilization_parts[4].rstrip('%')

        data.append([node_name, node_status, cpu_usage_percent, memory_usage_percent])

    return data
