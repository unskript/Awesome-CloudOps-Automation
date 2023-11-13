#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import pprint
import json
from typing import Tuple
from pydantic import BaseModel, Field
from tabulate import tabulate


try:
    from unskript.legos.kubernetes.k8s_utils import normalize_cpu, normalize_memory, normalize_storage
except Exception:
    pass


class InputSchema(BaseModel):
    threshold: int = Field(
        85,
        title='Threshold',
        description='Threshold in %age. Default is 85%'
    )

def k8s_get_nodes_with_insufficient_resources_printer(output):
    if output is None:
        return

    res_hdr = ["Name", "Resource"]
    data = []
    for o in output[1]:
        if isinstance(o, dict) is True:
            res_hdr = ["Name", "Allocatable", "Capacity"]
            data.append([
                o.get('name'),
                pprint.pformat(o.get('allocatable')),
                pprint.pformat(o.get('capacity'))
                ])        
    print(tabulate(data, headers=res_hdr, tablefmt='fancy_grid'))


def k8s_get_nodes_with_insufficient_resources(handle, threshold: int = 85) -> Tuple:
    """k8s_get_failed_deployments Returns the list of all failed deployments across all namespaces

    :type handle: object
    :param handle: Object returned from task.validate(...) method

    :type threshold: int
    :param threshold: Threshold in Percentage. Default value being 85.
                      Any node resource exceeding that threshold
                      is flagged as having insufficient resource.

    :rtype: Tuple of the result
    """
    retval = []

    # Get node information
    get_nodes_command = "kubectl get nodes -o=json"
    try:
        #response = subprocess.run(get_nodes_command.split(), capture_output=True, text=True, check=True)
        response = handle.run_native_cmd(get_nodes_command)
        nodes_info = json.loads(response.stdout)
    except Exception as e:
        raise Exception(f"Error fetching node information: {e.stderr}") from e

    for node_info in nodes_info['items']:
        node_name = node_info['metadata']['name']
        cpu_allocatable = normalize_cpu(node_info['status']['allocatable'].get('cpu', 0))
        cpu_capacity = normalize_cpu(node_info['status']['capacity'].get('cpu', 0))
        mem_allocatable = normalize_memory(node_info['status']['allocatable'].get('memory', 0))
        mem_capacity = normalize_memory(node_info['status']['capacity'].get('memory', 0))
        storage_allocatable = normalize_storage(node_info['status']['allocatable'].get('ephemeral-storage', 0))
        storage_capacity = normalize_storage(node_info['status']['capacity'].get('ephemeral-storage', 0))
        cpu_usage_percent = (cpu_capacity - cpu_allocatable) / cpu_capacity * 100
        mem_usage_percent = 0
        storage_usage_percent = 0
        if not storage_allocatable:
            storage_allocatable = 0
        if not mem_allocatable:
            mem_allocatable = 0

        if mem_capacity:
            mem_usage_percent = (mem_capacity - mem_allocatable) / mem_capacity * 100
        if storage_capacity:
            storage_usage_percent = (storage_capacity - storage_allocatable) / storage_capacity * 100


        if cpu_usage_percent >= threshold or mem_usage_percent >= threshold or storage_usage_percent >= threshold:
            retval.append({
                'name': node_name,
                'allocatable': node_info['status'].get('allocatable', {}),
                'capacity': node_info['status'].get('capacity', {})
            })


    if retval:
        return (False, retval)

    return (True, [])
