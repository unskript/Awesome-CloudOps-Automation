#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Tuple
from kubernetes import client
from kubernetes.client.rest import ApiException
from pydantic import BaseModel, Field
try:
    from unskript.legos.kubernetes.k8s_utils import normalize_cpu, normalize_memory
except:
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
    
    print(output)


def k8s_get_nodes_with_insufficient_resources(handle, threshold: int = 85) -> Tuple:
    """k8s_get_failed_deployments Returns the list of all failed deployments across all namespaces

    :type handle: Object
    :param handle: Object returned from task.validate(...) function

    :type threshold: int
    :param threshold: Threshold in Percentage. Default value being 85. Any node resource exceeding that threshold
                      is flagged as having insufficient resource.

    :rtype: Tuple of the result
    """
    if handle.client_side_validation != True:
        raise Exception(f"K8S Connector is invalid {handle}")

    api_client = client.CoreV1Api(api_client=handle)
    retval = []
    nodes = api_client.list_node().items
    for node in nodes:
        cpu_allocated = normalize_cpu(node.status.allocatable.get('cpu'))
        cpu_capacity = normalize_cpu(node.status.capacity.get('cpu'))
        mem_allocated = normalize_memory(node.status.allocatable.get('memory'))
        mem_capacity = normalize_memory(node.status.capacity.get('memory'))
        storage_allocated = normalize_memory(node.status.allocatable.get('ephemeral-storage'))
        storage_capacity = normalize_memory(node.status.capacity.get('ephemeral-storage'))
        if (cpu_allocated / cpu_capacity * 100) >= threshold \
            or (mem_allocated / mem_capacity * 100) >= threshold \
            or (storage_allocated / storage_capacity * 100) >= threshold:
            retval.append({'name': node.metadata.name, 'capacity': node.status.capacity})

    if  retval:
        return(False, retval)
    
    return (True, [])
