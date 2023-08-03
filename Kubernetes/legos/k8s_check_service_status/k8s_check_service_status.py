##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List, Tuple
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import json

# Disabling insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class InputSchema(BaseModel):
    namespace: str = Field(
        ...,
        description='Namespace in which the services are running.',
        title='K8s Namespace',
    )
    services: List = Field(
        ..., description='List of service names to be checked.', title='List of service names'
    )




def k8s_check_service_status_printer(output):
    if output is None:
        return
    print(output)


def get_service_url(service_name, namespace, handle):
    kubectl_command = f"kubectl get service {service_name} -n {namespace} -o=json"
    response = handle.run_native_cmd(kubectl_command)

    if response is None or response.stderr:
        error_message = response.stderr if response else "empty response"
        print(f"Error while executing command ({kubectl_command}) ({error_message})")
        return None

    service_info = json.loads(response.stdout)
    ip = service_info['spec']['clusterIP']
    port = service_info['spec']['ports'][0]['port']

    if ip and port:
        return f'http://{ip}:{port}'
    return None


def k8s_check_service_status(handle, services:list, namespace:str) -> Tuple:
    """
    k8s_check_service_status Checks the health status of the provided Kubernetes services.

    :type handle: object
    :param handle: Handle object to execute the kubectl command.

    :type services: list
    :param services: List of service names to be checked.

    :type namespace: str
    :param namespace: Namespace where the services reside.

    :return: Status, dictionary with service statuses.
    """
    status_dict = {}
    result = []

    for name in services:
        url = get_service_url(name, namespace, handle)

        if not url:
            print(f'Unable to find service {name}')
            continue

        # Check service health
        try:
            response = requests.get(url, verify=True, timeout=5)
            if response.status_code == 200:
                continue
            else:
                status_dict[name] = f'unhealthy. Status code: {response.status_code}'
                result.append(status_dict)
        except requests.RequestException as e:
            status_dict[name] = f'down. Error: {str(e)}'
            result.append(status_dict)

    if len(result) != 0:
        return (False, result)
    return (True, None)


