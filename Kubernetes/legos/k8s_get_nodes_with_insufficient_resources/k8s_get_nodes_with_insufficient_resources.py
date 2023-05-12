#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import pprint
from typing import Tuple
from pydantic import BaseModel, Field
from tabulate import tabulate
from kubernetes import client
from kubernetes.client.rest import ApiException

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

    :type handle: Object
    :param handle: Object returned from task.validate(...) function

    :type threshold: int
    :param threshold: Threshold in Percentage. Default value being 85.
    Any node resource exceeding that threshold
                      is flagged as having insufficient resource.

    :rtype: Tuple of the result
    """
    if handle.client_side_validation is not True:
        raise ApiException(f"K8S Connector is invalid {handle}")

    api_client = client.CoreV1Api(api_client=handle)
    retval = []
    nodes = api_client.list_node().items
    for node in nodes:
        cpu_allocatable = normalize_cpu(node.status.allocatable.get('cpu'))
        cpu_capacity = normalize_cpu(node.status.capacity.get('cpu'))
        mem_allocatable = normalize_memory(node.status.allocatable.get('memory'))
        mem_capacity = normalize_memory(node.status.capacity.get('memory'))
        storage_allocatable = normalize_storage(node.status.allocatable.get('ephemeral-storage'))
        storage_capacity = normalize_storage(node.status.capacity.get('ephemeral-storage'))
        cpu_usage_percent = (cpu_capacity - cpu_allocatable)/cpu_capacity * 100
        mem_usage_percent = (mem_capacity - mem_allocatable)/mem_capacity * 100
        storage_usage_percent = (storage_capacity - storage_allocatable)/storage_capacity * 100
        if cpu_usage_percent >= threshold \
            or mem_usage_percent >= threshold \
            or storage_usage_percent >= threshold:
            retval.append({
                'name': node.metadata.name,
                'allocatable': node.status.allocatable,
                'capacity': node.status.capacity
                })

    if  retval:
        return(False, retval)

    return (True, [])
