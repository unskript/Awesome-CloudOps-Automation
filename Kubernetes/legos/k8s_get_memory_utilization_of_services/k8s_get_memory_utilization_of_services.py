#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import os 
import json 

from typing import Optional, Tuple
from pydantic import BaseModel, Field
from tabulate import tabulate



class InputSchema(BaseModel):
    services: Optional[list] = Field(
        ...,
        description='List of pod names of the services for which memory utilization is to be fetched.',
        title='List of pod names (as services)',
    )
    namespace: Optional[str] = Field(
        ...,
        description='Namespace in which the services are running.',
        title='K8s Namespace',
    )
    threshold: Optional[float] = Field(
        80,
        description='Threshold for memory utilization percentage. Default is 80%.',
        title='Threshold (in %)',
    )
        
    
def k8s_get_memory_utilization_of_services_printer(output):
    status, data = output
    if status:
        print("All services are within memory utilization threhsold")
    else:
        headers = ["Service", "Namespace", "Utilization %"]
        table_data = []

        for entry in data:
            service = entry['service']
            namespace = entry['namespace']
            utilization_percentage = entry.get('utilization_percentage', "")
            table_data.append([service, namespace, utilization_percentage])
        print(tabulate(table_data, headers=headers, tablefmt="grid"))


def convert_memory_to_bytes(memory_value) -> int:
    if not memory_value:
        return 0
    units = {
        'K': 1000,
        'M': 1000 * 1000,
        'G': 1000 * 1000 * 1000,
        'T': 1000 * 1000 * 1000 * 1000,
        'Ki': 1024,
        'Mi': 1024 * 1024,
        'Gi': 1024 * 1024 * 1024,
        'Ti': 1024 * 1024 * 1024 * 1024,
    }

    for unit, multiplier in units.items():
        if memory_value.endswith(unit):
            return int(memory_value[:-len(unit)]) * multiplier

    return int(memory_value)

def k8s_get_memory_utilization_of_services(handle, namespace: str = "", threshold:float=80, services: list=[]) -> Tuple:
    """
    k8s_get_memory_utilization_of_services executes the given kubectl commands
    to find the memory utilization of the specified services in a particular namespace
    and compares it with a given threshold.

    :param handle: Object returned from the Task validate method, must have client-side validation enabled.
    :param namespace: Namespace in which the services are running.
    :param threshold: Threshold for memory utilization percentage. Default is 80%.
    :param services: List of pod names of the services for which memory utilization is to be fetched.
    :return: Status, list of exceeding services if any service has exceeded the threshold.
    """
    if handle.client_side_validation is False:
        raise Exception(f"K8S Connector is invalid: {handle}")

    if services and not namespace:
        raise ValueError("Namespace must be provided if services are specified.")

    if not namespace:
        namespace = 'default'

    exceeding_services = []

    # Main Idea:
    # 1. Given namespace, lets get current memory utilization for top pods
    # 2. Filter the list of pods to check from the service list
    # 3. For the pods get the memory request
    # 4. Calculate utilization as (mem_usage / mem_request) * 100
    # 5. Construct list of pods which has  Utilization > threshold  and return the list

    try:
        # Get memory utilization of all pods using top pods
        top_pods_command = f"kubectl top pods -n {namespace} --no-headers"
        response = handle.run_native_cmd(top_pods_command)
        top_pods_output = response.stdout.strip() 
        if not top_pods_output:
            raise ValueError(f"Top PODS data is empty for given namespace {namespace}")
        top_pods_output = top_pods_output.split('\n')
        pod_mem_util_dict = {x.split()[0]: x.split()[-1] for x in top_pods_output}

        pods_to_check = {}
        if services:
            # If services pod specified, lets iterate over it and check only for them.
            # If the mentioned pod not found in the top pod list, which means the memory
            # utilization is not significant, so dont need to check
            for svc_pod in services:
                if svc_pod in pod_mem_util_dict.keys():
                    pods_to_check[svc_pod] = pod_mem_util_dict[svc_pod]

        if not pods_to_check:
            pods_to_check = pod_mem_util_dict

        for pod, mem_usage in pods_to_check.items():
            kubectl_command = f"kubectl get pod {pod} -n {namespace} -o=jsonpath='{{.spec.containers[0].resources.requests.memory}}'"
            response = handle.run_native_cmd(kubectl_command)
            mem_request = response.stdout.strip()
            mem_usage = pod_mem_util_dict.get(pod)

            mem_usage = convert_memory_to_bytes(mem_usage)
            mem_request = convert_memory_to_bytes(mem_request)

            if not mem_request:
                # Memory limit is not set, so lets continue with the execution
                continue
            utilization = (mem_usage / mem_request if mem_request else 1) * 100
            utilization = round(utilization, 2)
            if utilization > threshold:
                exceeding_services.append({
                    "service": pod,
                    "namespace": namespace,
                    "utilization_percentage": utilization
                })
    except Exception as e:
        raise e

    return (False, exceeding_services) if exceeding_services else (True, [])