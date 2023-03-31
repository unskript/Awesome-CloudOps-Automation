#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Tuple
from kubernetes import client
from kubernetes.client.rest import ApiException
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    pass

def k8s_get_nodes_with_insufficient_resources_printer(output):
    if output is None:
        return 
    
    print(output)


def k8s_get_nodes_with_insufficient_resources(handle) -> Tuple:
    """k8s_get_failed_deployments Returns the list of all failed deployments across all namespaces

    :type handle: Object
    :param handle: Object returned from task.validate(...) function

    :rtype: Tuple of the result
    """
    if handle.client_side_validation != True:
        raise Exception(f"K8S Connector is invalid {handle}")

    api_client = client.CoreV1Api(api_client=handle)
    retval = []
    nodes = api_client.list_node().items
    for node in nodes:
        if node.status.allocatable.cpu < node.status.capacity.cpu \
            or node.status.allocatable.memory < node.status.capacity.memory \
            or node.status.allocatable.storage < node.status.capacity.storage:
            retval.append(node)
    
    if not retval:
        return(True, [])
    
    return (False, retval)
