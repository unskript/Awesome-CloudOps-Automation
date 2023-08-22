#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from tabulate import tabulate
from kubernetes.client.rest import ApiException



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



def convert_memory_to_milli(memory_request: str) -> int:
    units = {
        'K': 1,
        'M': 1000,
        'G': 1000 * 1000,
        'T': 1000 * 1000 * 1000,
    }

    if memory_request[-1] in units:
        return int(memory_request[:-1]) * units[memory_request[-1]]
    elif memory_request[-2:] == 'Ki':
        return int(memory_request[:-2])
    elif memory_request[-2:] == 'Mi':
        return int(memory_request[:-2]) * 1000
    elif memory_request[-2:] == 'Gi':
        return int(memory_request[:-2]) * 1000 * 1000
    elif memory_request[-2:] == 'Ti':
        return int(memory_request[:-2]) * 1000 * 1000 * 1000
    else:
        return int(memory_request)



def k8s_get_memory_utilization_of_services(handle, namespace: str = "", threshold:float=80, services: list="") -> Tuple:
    """
    k8s_get_memory_utilization_of_services executes the given kubectl commands
    to find the memory utilization of the specified services in a particular namespace
    and compares it with a given threshold.

    Example-
    Memory Request: The memory request for the service is 256Mi, and the function convert_memory_to_milli converts this value to 256000 milli units.
    Memory Usage: According to the kubectl top pod command, the memory usage for the container is 4Mi, which equals 4000 milli units (since 1 Mi = 1000 milli units).
    Utilization Percentage Calculation: The utilization percentage would be calculated as (memory_usage / memory_request_milli) * 100.
    Substituting the values we have:
    (4000/256000)∗100=0.0015625∗100=0.15625% (Utilization %)

    :type handle: object
    :param handle: Object returned from the Task validate method, must have client-side validation enabled.

    :type services: list
    :param services: List of pod names of the services for which memory utilization is to be fetched.

    :type namespace: str
    :param namespace: Namespace in which the services are running.

    :type threshold: float, optional
    :param threshold: Threshold for memory utilization percentage. Default is 80%.

    :rtype: tuple (status, list of exceeding services or None)
    :return: Status, list of exceeding services if any service has exceeded the threshold,
    """
    if handle.client_side_validation is False:
        raise ApiException(f"K8S Connector is invalid: {handle}")

    if services and not namespace:
        raise ApiException("Namespace must be provided if services are specified.")

    if not namespace:
        kubectl_command = "kubectl get namespace -o=jsonpath='{.items[*].metadata.name}'"
        response = handle.run_native_cmd(kubectl_command)
        if response is None or response.stderr:
            raise ApiException(f"Error occurred while executing command {kubectl_command} {response.stderr if response else 'empty response'}")
        namespaces = response.stdout.strip().split(' ')
    else:
        namespaces = [namespace]

    exceeding_services = []

    for nmspace in namespaces:
        if not services:
            kubectl_command = f"kubectl get pods -n {nmspace} -o=jsonpath='{{.items[*].metadata.name}}'"
            response = handle.run_native_cmd(kubectl_command)
            if response is None or response.stderr:
                raise ApiException(f"Error occurred while executing command {kubectl_command} {response.stderr if response else 'empty response'}")
            services_to_check = response.stdout.strip().split(' ')
        else:
            services_to_check = services

        for service in services_to_check:
            # Get the memory request for the service
            kubectl_command = f"kubectl get pod {service} -n {nmspace} -o=jsonpath='{{.spec.containers[0].resources.requests.memory}}'"
            response = handle.run_native_cmd(kubectl_command)
            memory_request = response.stdout

            memory_request = memory_request.strip() if memory_request else '0'
            memory_request_milli = convert_memory_to_milli(memory_request)
            if memory_request_milli == 0:
                print(f"Warning: Memory request usage not set for '{service}' in '{nmspace}' namespace")
            # Get the memory usage for the service
            kubectl_command = f"kubectl top pod {service} -n {nmspace} --containers | awk '{{print $3}}' | tail -n +2"
            response = handle.run_native_cmd(kubectl_command)
            memory_usage_values = response.stdout.strip().split('\n')
            memory_usage_values = [int(value.replace('m', '')) * 1024 if 'm' in value else int(value) for value in memory_usage_values if value.strip()]

            # Compare each memory usage with the threshold and add to exceeding_services if necessary
            for memory_usage in memory_usage_values:
                utilization_percentage = (memory_usage / memory_request_milli) * 100 if memory_request_milli > 0 else 0
                if utilization_percentage > threshold:
                    exceeding_services.append({"service": service, "namespace": nmspace,"message": "Memory request usage not set", "utilization_percentage": utilization_percentage})

    if exceeding_services:
        return (False, exceeding_services)
    return (True, None)


