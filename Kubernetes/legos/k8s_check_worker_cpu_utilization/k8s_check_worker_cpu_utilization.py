from __future__ import annotations

#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from pydantic import BaseModel, Field
from typing import Optional, Tuple



class InputSchema(BaseModel):
    threshold: Optional[float] = Field(
        70.0,
        description='Threshold for CPU utilization in percentage.',
        title='Threshold (in %)',
    )


def k8s_check_worker_cpu_utilization_printer(output):
    status, nodes_info = output
    if status:
        print("All nodes are within the CPU utilization threshold.")
        return

    print("ALERT: Nodes exceeding CPU utilization threshold:")
    print("-" * 40)
    for node_info in nodes_info:
        print(f"Node: {node_info['node']} - CPU Utilization: {node_info['cpu']}%")
    print("-" * 40)

def k8s_check_worker_cpu_utilization(handle, threshold: float=70.0) -> Tuple:
    """
    k8s_check_worker_cpu_utilization Retrieves the CPU utilization for all worker nodes in the cluster and compares it to a given threshold.

    :type handle: object
    :param handle: Handle object to execute the kubectl command.

    :type threshold: int
    :param threshold: Threshold for CPU utilization in percentage.

    :return: Status and dictionary with node names and their CPU information if any node's CPU utilization exceeds the threshold.
    """
    exceeding_nodes = []
    kubectl_command = "kubectl top nodes --no-headers"
    response = handle.run_native_cmd(kubectl_command)

    if response is None or response.stderr:
        raise Exception(f"Error while executing command ({kubectl_command}): {response.stderr if response else 'empty response'}")

    lines = response.stdout.split('\n')
    for line in lines:
        parts = line.split()
        if len(parts) < 5:  # Check for correct line format
            continue
        node_name, cpu_percentage_str = parts[0], parts[2]
        cpu_percentage = float(cpu_percentage_str.rstrip('%'))

        if cpu_percentage > threshold:
            exceeding_nodes.append({"node": node_name, "cpu": cpu_percentage})

    if len(exceeding_nodes) != 0:
        return (False, exceeding_nodes)
    return (True, None)



