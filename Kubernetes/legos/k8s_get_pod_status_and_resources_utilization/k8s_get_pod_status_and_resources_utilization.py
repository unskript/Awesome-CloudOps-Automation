
#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Optional, Dict
from tabulate import tabulate
import json
from kubernetes.client.rest import ApiException
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    namespace: Optional[str] = Field('', description='k8s Namespace', title='Namespace')


def k8s_get_pod_status_and_resources_utilization_printer(data):
    # print the data
    for resource, rows in data.items():
        print(f"\n{resource.capitalize()}:")
        if resource == 'pods':
            headers = ['Name', 'Status', 'CPU Usage', 'Memory Usage (MB)', 'Disk Usage (MB)']
        else:
            headers = ['Name', 'Status']
        print(tabulate(rows, headers, tablefmt='pretty'))

def k8s_get_pod_status_and_resources_utilization(handle, namespace:str="") -> Dict:
    """
    k8s_get_all_resources_utilization_info fetches the pod status and resource utilization of various Kubernetes resources like jobs, services, persistent volumes.

    :type handle: object
    :param handle: Object returned from the Task validate method

    :type namespace: string
    :param namespace: Namespace in which to look for the resources. If not provided, all namespaces are considered

    :rtype: Status, Message
    """

    if handle.client_side_validation is not True:
        print(f"K8S Connector is invalid: {handle}")
        return False, "Invalid Handle"

    namespace_option = f"--namespace={namespace}" if namespace else "--all-namespaces"

    resources = ['pods', 'jobs', 'persistentvolumeclaims']
    data = {resource: [] for resource in resources}

    for resource in resources:
        cmd = f"kubectl get {resource} -o json {namespace_option}"
        result = handle.run_native_cmd(cmd)

        if result.stderr:
            raise ApiException(f"Error occurred while executing command {cmd} {result.stderr}")

        items = json.loads(result.stdout)['items']

        for item in items:
            name = item['metadata']['name']
            status = 'Unknown'

            if resource == 'pods':
                status = item['status']['phase']

                resources = item['spec']['containers'][0].get('resources', {})
                requests = resources.get('requests', {})

                cpu_usage = requests.get('cpu', 'N/A')
                memory_usage = int(requests.get('memory', '0Ki').rstrip('Ki')) / 1024 if 'Ki' in requests.get('memory', '') else 'N/A' # if in KiB
                disk_usage = int(requests.get('ephemeral-storage', '0Ki').rstrip('Ki')) / 1024 if 'Ki' in requests.get('ephemeral-storage', '') else 'N/A' # if in KiB

                data[resource].append([name, status, cpu_usage, memory_usage, disk_usage])
            else:
                if resource == 'jobs':
                    conditions = item['status'].get('conditions', [])
                    if conditions:
                        status = conditions[-1]['type']
                elif resource == 'persistentvolumeclaims':
                    status = item['status']['phase']

                data[resource].append([name, status])

    return data



