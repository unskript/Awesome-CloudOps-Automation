##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from tabulate import tabulate
from kubernetes import client

pp = pprint.PrettyPrinter(indent=2)

class InputSchema(BaseModel):
    cpu_limit: Optional[int] = Field(
        default=0,
        title='CPU Limit',
        description='CPU Limit. Eg 2')
    memory_limit: Optional[str] = Field(
        default="",
        title='Memory Limit (Mi)',
        description='Limits and requests for memory are measured in bytes. '
                    'Accept the store in Mi. Eg 123Mi')
    pod_limit: Optional[int] = Field(
        default=0,
        title='Number of Pods to attach',
        description='Pod Limit. Eg 2')


def k8s_get_candidate_nodes_for_pods_printer(output):
    if output is None:
        return

    data = output[0]
    print("\n")
    print(tabulate(data, tablefmt="grid", headers=[
        "Name",
        "cpu",
        "ephemeral-storage",
        "hugepages-1Gi",
        "hugepages-2Mi",
        "memory",
        "pods"
        ]))

def k8s_get_candidate_nodes_for_pods(handle,
                                     cpu_limit: int = 0,
                                     memory_limit: str = "",
                                     pod_limit: int = 0) -> Tuple:

    """k8s_get_candidate_nodes_for_pods get nodes for pod

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type cpu_limit: int
        :param cpu_limit: CPU Limit.

        :type memory_limit: string
        :param memory_limit: Limits and requests for memory are measured in bytes.

        :type pod_limit: int
        :param pod_limit: Pod Limit.

        :rtype: Tuple of nodes for pod
    """

    coreApiClient = client.CoreV1Api(api_client=handle)

    nodes = coreApiClient.list_node()
    match_nodes = [node for node in nodes.items if
                   (cpu_limit < int(node.status.capacity.get("cpu", 0))) and
                   (pod_limit < int(node.status.capacity.get("pods", 0))) and
                   int(memory_limit.split("Mi")[0]) < (int(node.status.capacity.get("memory").split("Ki")[0]) / 1024)]

    if len(match_nodes) > 0:
        data = []
        for node in match_nodes:
            node_capacity = []
            node_capacity.append(node.metadata.name)
            for capacity in node.status.capacity.values():
                node_capacity.append(capacity)
            data.append(node_capacity)

        return (data, match_nodes)

    pp.pprint("No Matching Nodes Found for this spec")
    return (None, None)
