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



def convert_memory_to_bytes(memory_value: str) -> int:
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

def parse_pod_data(data):
    if not data:
        return []
    
    parsed_data = []

    for item in data.get('items', []):
        pod_info = {
            'name': item['metadata']['name'],
            'namespace': item['metadata']['namespace'],
            'labels': item['metadata'].get('labels', {}),
            'annotations': item['metadata'].get('annotations', {}),
            'status': item['status']['phase'],
            'containers': [],
            'spec': item.get('spec', {})
        }

        for container in pod_info['spec'].get('containers', []):
            container_info = {
                'name': container['name'],
                'namespace': item['metadata']['namespace'],
                'image': container['image'],
                'resources': container.get('resources', {})
            }
            resources = container_info['resources']
            container_info['memory_request'] = resources.get('requests', {}).get('memory', None)
            container_info['memory_limit'] = resources.get('limits', {}).get('memory', None)
            container_info['cpu_request'] = resources.get('requests', {}).get('cpu', None)
            container_info['cpu_limit'] = resources.get('limits', {}).get('cpu', None)

            parsed_data.append(container_info)

    return parsed_data


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
    try:
        json_data = {}
        if not services:
            kubectl_command = f"kubectl get pods -n {namespace} -o json"
            response = handle.run_native_cmd(kubectl_command)
            json_data = json.loads(response.stdout.strip())
        else:
            service_pods = " ".join(services)
            kubectl_command = f"kubectl get pods -n {namespace} {service_pods} -o json"
            response = handle.run_native_cmd(kubectl_command)
            json_data = json.loads(response.stdout.strip())
        
        pod_data = parse_pod_data(json_data)
        for data in pod_data: 
            mem_usage = convert_memory_to_bytes(data.get('memory_request')) 
            mem_limit = convert_memory_to_bytes(data.get('memory_limit'))
            if not mem_limit:
                # Memory limit is not set, so lets continue with the execution
                continue
            utilization = (mem_usage / mem_limit if mem_limit else 1) * 100
            utilization = round(utilization, 2)
            if utilization > threshold:
                exceeding_services.append({
                    "service": data.get('name'),
                    "namespace": data.get('namespace'),
                    "utilization_percentage": utilization
                })
    except Exception as e:
        raise e

    return (False, exceeding_services) if exceeding_services else (True, [])
