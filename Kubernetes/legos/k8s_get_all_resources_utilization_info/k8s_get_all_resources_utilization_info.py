
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
    pod_utilization_cmd = f"kubectl top pods {namespace_option} --no-headers"
    pod_utilization = handle.run_native_cmd(pod_utilization_cmd)
    if pod_utilization.stderr:
        print(f"Error occurred while fetching pod utilization: {pod_utilization.stderr}")
        pass

    pod_utilization_lines = pod_utilization.stdout.split('\n')
    utilization_map = {}
    for line in pod_utilization_lines:
        parts = line.split()
        if len(parts) < 3:  # Skip if line doesn't contain enough parts
            continue
        pod_name = parts[0]
        cpu_usage = parts[1]
        memory_usage = parts[2]
        # Use a tuple of (namespace, pod_name) as the key to ensure uniqueness across namespaces
        key = (namespace, pod_name) if namespace else (parts[0], pod_name)  # Adjust according to your needs
        utilization_map[key] = (cpu_usage, memory_usage)

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
                key = (ns, name)
                cpu_usage, memory_usage = utilization_map.get(key, ('N/A', 'N/A'))
                data[resource].append([ns, name, status, cpu_usage, memory_usage])
            else:
                if resource == 'jobs':
                    conditions = item['status'].get('conditions', [])
                    if conditions:
                        status = conditions[-1]['type']
                elif resource == 'persistentvolumeclaims':
                    status = item['status']['phase']
                data[resource].append([ns, name, status])

    return data
