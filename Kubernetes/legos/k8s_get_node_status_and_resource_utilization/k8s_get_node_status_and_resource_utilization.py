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
        headers = ['Node Name', 'Status', 'CPU Usage', 'Memory Usage(Mi)', 'Disk Usage(Mi)']
        print(tabulate(output, headers, tablefmt='pretty'))


def k8s_get_node_status_and_resource_utilization(handle)-> List:
    """k8s_get_node_status_and_resource_utilization fetches resource utilization on nodes

        :type handle: object
        :param handle: Object returned from the Task validate method

        :rtype: Node information, and resource utiliation information
    """
    if handle.client_side_validation is not True:
        print(f"K8S Connector is invalid: {handle}")
        return False, "Invalid Handle"

    # Create the kubectl command for fetching node status
    node_status_cmd = "kubectl get nodes -o json"

    # Execute the kubectl command for fetching node status
    node_status = handle.run_native_cmd(node_status_cmd)
    if node_status.stderr:
        raise ApiException(f"Error occurred while executing command {node_status_cmd} {node_status.stderr}")

    nodes_info = json.loads(node_status.stdout)

    data = []
    for item in nodes_info['items']:
        node_name = item['metadata']['name']
        # Get the latest status by considering the last condition in the list
        node_status = item['status']['conditions'][-1]['type']
        cpu_usage = item['status']['capacity']['cpu']
        memory_usage = int(item['status']['capacity']['memory'].rstrip('Ki')) / 1024  # if in KiB
        disk_usage = int(item['status']['capacity']['ephemeral-storage'].rstrip('Ki')) / 1024  # if in KiB

        data.append([node_name, node_status, cpu_usage, memory_usage, disk_usage])  # Add disk_usage if available.

    return data


