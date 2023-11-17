#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Optional, Tuple
from pydantic import BaseModel, Field
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

    :type handle: object
    :param handle: Object returned from the task.validate(...)

    :type namespace: str
    :param namespace: (Optional) String, K8S Namespace as python string

    :type tail_lines: int
    :param tail_lines: Number of log lines to fetch from each container. Defaults to 100.

    :rtype: Status, List of objects of pods, namespaces that might have crashed along with the timestamp
    """
    ERROR_PATTERNS = [
        "Worker exiting",
        "Exception",
        "Exception in worker process"
        # Add more error patterns here as necessary
    ]
    crash_logs = []

    # If namespace not provided, assume it to be the default namespace
    if not namespace:
        namespace = "default"

    get_services_command = f"kubectl get svc -n {namespace} -o=jsonpath={{.items[*].metadata.name}}"
    try:
        # Execute the kubectl command to get service names
        response = handle.run_native_cmd(get_services_command)
        service_names = response.stdout.strip().split()
    except Exception as e:
        raise Exception(f"Error fetching service names: {e.stderr}") from e

    if not isinstance(service_names, list):
        service_names = [service_names]

    visited_pods = []
    for service_name in service_names:
        # Get service's pod based on its labels
        get_service_labels_command = f"kubectl get service {service_name} -n {namespace} -o=jsonpath={{.spec.selector}}"
        try:
            # Execute the kubectl command to get service labels
            response = handle.run_native_cmd(get_service_labels_command)
            if not response.stdout.strip():
                # No labels found for a particular service. Skipping...
                continue
            labels_dict = json.loads(response.stdout.replace("'", "\""))
            label_selector = ",".join([f"{k}={v}" for k, v in labels_dict.items()])
        except Exception as e:
            raise Exception(f"Error while fetching labels for service {service_name}: {e.stderr}") from e

        # Fetch the pod attached to this service along and its container
        pod_and_container_cmd = f"kubectl get pods -n {namespace} -l {label_selector}" + " -o=jsonpath=\"{range .items[*]}{.metadata.name}:{range .spec.containers[*]}{.name}{' '}{end}{end}\""
        try:
            # Execute the kubectl command to get pod name
            response = handle.run_native_cmd(pod_and_container_cmd)
            if not response.stdout.strip():
                # No pods found for a particular service. Skipping...
                continue
            pod_name_with_container = response.stdout.strip()
        except Exception as e:
            raise Exception(f"Error while fetching pod for service {service_name}: {e.stderr}") from e

        p_and_c_list = []
        if not isinstance(pod_name_with_container, list):
            if len(pod_name_with_container.split(':')) > 2:
                for pc in pod_name_with_container.split(' '):
                    p_and_c_list.append(pc)
            else:
                p_and_c_list = [pod_name_with_container]

        for pod_and_container in p_and_c_list:
            pod_name, container = pod_and_container.split(':')
            if pod_name in visited_pods:
                continue

            visited_pods.append(pod_name)
            # Fetch and analyze logs for the given pod
            for c in container.split(' '):
                log_cmd = f"kubectl logs {pod_name} -c {c} -n {namespace} --tail={tail_lines}"
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
                                        "namespace": namespace,
                                        "error": pattern,
                                        "timestamp": timestamp,
                                    })
                except Exception as e:
                    print(f"Error while fetching logs for pod {pod_name}: {e}")

    return (False, crash_logs) if crash_logs else (True, None)