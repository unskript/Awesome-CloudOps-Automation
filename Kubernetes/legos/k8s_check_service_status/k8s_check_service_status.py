##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List, Tuple, Optional
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import json

# Disabling insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        ...,
        description='Namespace in which the services are running.',
        title='K8s Namespace',
    )
    services: Optional[List] = Field(
        ..., description='List of service names to be checked.', title='List of service names'
    )


def k8s_check_service_status_printer(output):

    status, result = output
    if status:
        print("All services are healthy.")
        return

    # If there are any unhealthy services
    print("\n" + "=" * 100)  # main separator

    for service, status_msg in result[0].items():
        print(f"Service:\t{service}")
        print("-" * 100)  # sub-separator
        print(f"Status: {status_msg}\n")
        print("=" * 100)  # main separator


def get_service_url(service_name, namespace, handle):
    kubectl_command = f"kubectl get service {service_name} -n {namespace} -o=json"
    response = handle.run_native_cmd(kubectl_command)

    if response is None or response.stderr:
        error_message = response.stderr if response else "empty response"
        print(f"Error while executing command ({kubectl_command}) ({error_message})")
        return None

    service_info = json.loads(response.stdout)

    # Check if 'spec' key exists in service_info
    if 'spec' not in service_info:
        print(f"Service '{service_name}' in namespace '{namespace}' does not contain 'spec' key.")
        return None

    ip = service_info['spec'].get('clusterIP', None)
    port = None
    if 'ports' in service_info['spec'] and len(service_info['spec']['ports']) > 0:
        port = service_info['spec']['ports'][0].get('port', None)

    if ip and port:
        return f'http://{ip}:{port}'
    return None


def k8s_check_service_status(handle, services: list = "", namespace: str = "") -> Tuple:
    """
    k8s_check_service_status Checks the health status of the provided Kubernetes services.

    :type handle: object
    :param handle: Handle object to execute the kubectl command.

    :type services: list, optional
    :param services: List of service names to be checked.

    :type namespace: str, optional
    :param namespace: Namespace where the services reside.

    :return: Status, dictionary with service statuses.
    """
    status_dict = {}
    result = []

    # Get all namespaces if none is provided
    if not namespace:
        kubectl_command = "kubectl get namespace -o=jsonpath='{.items[*].metadata.name}'"
        response = handle.run_native_cmd(kubectl_command)
        if response is None or response.stderr:
            raise ValueError(f"Error occurred while executing command {kubectl_command} {response.stderr if response else 'empty response'}")
        namespaces = response.stdout.strip().split(' ')
    else:
        namespaces = [namespace]

    # For each namespace
    for ns in namespaces:
        # If services are provided
        if services or len(services)!=0:
            services_to_check = services
        else:
            kubectl_command = f"kubectl get services -n {ns} -o=jsonpath='{{.items[*].metadata.name}}'"
            response = handle.run_native_cmd(kubectl_command)
            if response is None or response.stderr:
                print(f"Error occurred while executing command {kubectl_command} {response.stderr if response else 'empty response'}")
                continue
            services_to_check = response.stdout.strip().split(' ')

        for name in services_to_check:
            url = get_service_url(name, ns, handle)

            if not url:
                print(f'Unable to find service {name} in namespace {ns}')
                continue

            # Check service health
            try:
                response = requests.get(url, verify=True, timeout=5)
                if response.status_code != 200:
                    status_dict[name] = f'unhealthy in namespace {ns}. Status code: {response.status_code}'
                    result.append(status_dict)
            except requests.RequestException as e:
                status_dict[name] = f'down in namespace {ns}. Error: {str(e)}'
                result.append(status_dict)

    if len(result) != 0:
        return (False, result)
    return (True, None)