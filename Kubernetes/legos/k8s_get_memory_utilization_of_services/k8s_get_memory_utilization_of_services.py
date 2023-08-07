#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from kubernetes.client.rest import ApiException
from pprint import pprint


class InputSchema(BaseModel):
    services: list = Field(
        ...,
        description='List of pod names of the services for which memory utilization is to be fetched.',
        title='List of pod names (as services)',
    )
    namespace: str = Field(
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
    if output is None:
        return
    pprint(output)



def k8s_get_memory_utilization_of_services(handle, services: list, namespace: str, threshold:float=80) -> Tuple:
    """
    k8s_get_memory_utilization_of_services executes the given kubectl commands
    to find the memory utilization of the specified services in a particular namespace
    and compares it with a given threshold.

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

    exceeding_services = []

    for service in services:
        # Get the memory request for the service
        kubectl_command = f"kubectl get pod {service} -n {namespace} -o=jsonpath='{{.spec.containers[0].resources.requests.memory}}'"
        response = handle.run_native_cmd(kubectl_command)
        if response is None:
            print(f"Error while executing command ({kubectl_command}) (empty response)")
            return False, None
        if response.stderr:
            raise ApiException(f"Error occurred while executing command {kubectl_command} {response.stderr}")
        memory_request = response.stdout

        # Get the memory usage for the service
        kubectl_command = f"kubectl top pod {service} -n {namespace} --containers | awk '{{print $3}}' | tail -n +2"
        response = handle.run_native_cmd(kubectl_command)
        if response.stderr:
            raise ApiException(f"Error occurred while executing command {kubectl_command} {response.stderr}")

        memory_usage_values = response.stdout.strip().split('\n')
        memory_usage_values = [int(value.replace('m', '')) for value in memory_usage_values if value]

        # Convert memory_request to milli-units and check for zero request
        memory_request_milli = int(memory_request) * 1000 if memory_request else 0
        if memory_request_milli == 0:
            exceeding_services.append({"service": service, "namespace": namespace, "message": "Memory request usage not set"})

        # Compare each memory usage with the threshold and add to exceeding_services if necessary
        for memory_usage in memory_usage_values:
            utilization_percentage = (memory_usage / memory_request_milli) * 100 if memory_request_milli > 0 else 0
            if utilization_percentage > threshold:
                print(f"Warning: Service {service} in namespace {namespace} has exceeded the memory utilization threshold of {threshold}%. Memory Usage: {utilization_percentage}%.")
                exceeding_services.append({"service": service, "namespace": namespace, "utilization_percentage": utilization_percentage})

    if exceeding_services:
        return (False, exceeding_services)
    return (True, None)


