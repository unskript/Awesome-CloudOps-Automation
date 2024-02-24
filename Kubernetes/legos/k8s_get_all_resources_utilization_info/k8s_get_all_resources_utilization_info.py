
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


def k8s_get_all_resources_utilization_info_printer(data):
    namespace = data['namespace']
    for resource, rows in data.items():
        if resource == 'namespace':  # Skip the namespace key-value pair
            continue

        print(f"\n{resource.capitalize()}:")
        if not rows:  # Check if the resource list is empty
            print(f"No {resource} found in {namespace} namespace.")
            continue  # Skip to the next resource

        if resource == 'pods':
            headers = ['Namespace', 'Name', 'Status', 'CPU Usage (m)', 'Memory Usage (Mi)']
        else:
            headers = ['Name', 'Status']
        print(tabulate(rows, headers, tablefmt='pretty'))


def k8s_get_all_resources_utilization_info(handle, namespace: str = "") -> Dict:
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
    data['namespace'] = namespace  # Store namespace in data dict

    # Fetch current utilization of pods
    pod_utilization_cmd = f"kubectl top pods {namespace_option}"
    pod_utilization = handle.run_native_cmd(pod_utilization_cmd)
    pod_utilization_lines = pod_utilization.stdout.split('\n')[1:]  # Exclude header line

    utilization_map = {}
    for line in pod_utilization_lines:
        parts = line.split()
        if len(parts) < 4:  # Skip lines that do not contain enough information
            continue
        utilization_map[parts[1]] = (parts[0], parts[2], parts[3])  # Map pod name to (namespace, CPU, Memory)

    for resource in resources:
        cmd = f"kubectl get {resource} -o json {namespace_option}"
        result = handle.run_native_cmd(cmd)

        if result.stderr:
            print(f"Error occurred while executing command {cmd}: {result.stderr}")
            continue 

        items = json.loads(result.stdout)['items']
        if not items:  # If no items found, continue to ensure message is printed by printer function
            continue

        for item in items:
            name = item['metadata']['name']
            ns = item['metadata'].get('namespace', 'default')
            status = 'Unknown'

            if resource == 'pods':
                status = item['status']['phase']
                ns_from_util, cpu_usage, memory_usage = utilization_map.get(name, (ns, 'N/A', 'N/A'))

                data[resource].append([ns_from_util, name, status, cpu_usage, memory_usage])
            else:
                if resource == 'jobs':
                    conditions = item['status'].get('conditions', [])
                    if conditions:
                        status = conditions[-1]['type']
                elif resource == 'persistentvolumeclaims':
                    status = item['status']['phase']

                data[resource].append([name, status])

    return data
