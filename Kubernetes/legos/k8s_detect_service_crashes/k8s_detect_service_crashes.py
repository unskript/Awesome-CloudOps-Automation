#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException
from tabulate import tabulate 
import json

class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        '',
        description='K8S Namespace',
        title='K8S Namespace'
    )
    tail_lines: Optional[int] = Field(
        100,
        description='Number of log lines to fetch from each container. Defaults to 100.',
        title='No. of lines (Default: 100)'
    )



ERROR_PATTERNS = [
    "Worker exiting",
    "Exception",
    "Exception in worker process"
    # Add more error patterns here as necessary
]

def k8s_detect_service_crashes_printer(output):
    status, data = output

    if status:
        print("No detected errors in the logs of the pods.")
    else:
        headers = ["Pod", "Namespace", "Error", "Timestamp"]
        table_data = [(entry["pod"], entry["namespace"], entry["error"], entry["timestamp"]) for entry in data]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))


def k8s_detect_service_crashes(handle, namespace: str = '', tail_lines: int = 100) -> Tuple:
    """
    k8s_detect_service_crashes detects service crashes by checking the logs of each pod for specific error messages.

    :type handle: Object
    :param handle: Object returned from the task.validate(...) function

    :type namespace: str
    :param namespace: (Optional) String, K8S Namespace as python string

    :type tail_lines: int
    :param tail_lines: Number of log lines to fetch from each container. Defaults to 100.

    :rtype: Status, List of objects of pods, namespaces that might have crashed along with the timestamp
    """
    crash_logs = []

    if handle.client_side_validation is not True:
        raise ApiException(f"K8S Connector is invalid {handle}")

    v1 = client.CoreV1Api(api_client=handle) 

    namespaces_to_check = [namespace] if namespace else [ns.metadata.name for ns in v1.list_namespace().items]

    for ns in namespaces_to_check:

        # Get all services in the namespace
        get_all_services_command = f"kubectl get svc -n {ns} -o=jsonpath='{{.items[*].metadata.name}}'"
        response = handle.run_native_cmd(get_all_services_command)
        if not response or response.stderr:
            raise ApiException(f"Error fetching services in namespace {ns}: {response.stderr if response else 'empty response'}")
        services_to_check = response.stdout.strip().split()

        for svc in services_to_check:

            # Get service's pod based on its labels
            get_service_labels_command = f"kubectl get service {svc} -n {ns} -o=jsonpath='{{.spec.selector}}'"
            response = handle.run_native_cmd(get_service_labels_command)
            if not response.stdout.strip():
                # No labels found for a particular service. Skipping... 
                continue
            labels_dict = json.loads(response.stdout.replace("'", "\""))
            label_selector = ",".join([f"{k}={v}" for k, v in labels_dict.items()])

            # Fetch the pod attached to this service
            get_pod_command = f"kubectl get pods -n {ns} -l {label_selector} -o=jsonpath='{{.items[0].metadata.name}}'"
            response = handle.run_native_cmd(get_pod_command)
            if not response or response.stderr:
                raise ApiException(f"Error while executing command ({get_pod_command}): {response.stderr if response else 'empty response'}")
            pod_name = response.stdout.strip()

            # Get the full pod object
            try:
                pod = v1.read_namespaced_pod(name=pod_name, namespace=ns)
            except ApiException as e:
                raise ApiException(f"Error fetching pod {pod_name} in namespace {ns}: {str(e)}")

            # Fetch and analyze logs for the given pod
            containers = [c.name for c in pod.spec.containers]
            for container_name in containers:
                log_cmd = f"kubectl logs {pod_name} -n {ns} -c {container_name} --tail={tail_lines}"
                try:
                    response = handle.run_native_cmd(log_cmd)
                    if response and not response.stderr:
                        log_output = response.stdout.splitlines()
                        for line in log_output:
                            for pattern in ERROR_PATTERNS:
                                if pattern in line:
                                    timestamp = line.split(']')[0].strip('[').split()[0] if ']' in line else "Unknown Time"
                                    crash_logs.append({
                                        "pod": pod_name,
                                        "namespace": ns,
                                        "error": pattern,
                                        "timestamp": timestamp,
                                    })
                except Exception as e:
                    print(f"Error while fetching logs for pod {pod_name} container {container_name}: {str(e)}")

    return (False, crash_logs) if crash_logs else (True, None)