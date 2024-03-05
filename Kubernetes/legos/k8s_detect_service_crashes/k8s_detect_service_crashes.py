#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import json
import re

from typing import Optional, Tuple
from pydantic import BaseModel, Field
from tabulate import tabulate 

class InputSchema(BaseModel):
    namespace: str = Field(
        description='K8S Namespace',
        title='K8S Namespace'
    )
    tail_lines: Optional[int] = Field(
        100,
        description='Number of log lines to fetch from each container. Defaults to 100.',
        title='No. of lines (Default: 100)'
    )
    services_to_detect_crashes: list = Field(
        description='List of services to detect service crashes on.'
    )

def k8s_detect_service_crashes_printer(output):
    status, data = output

    if status:
        print("No detected errors in the logs of the pods.")
    else:
        headers = ["Pod", "Namespace", "Error", "Timestamp"]
        table_data = [(entry["pod"], entry["namespace"], entry["error"], entry["timestamp"]) for entry in data]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))



def k8s_detect_service_crashes(handle, namespace: str, services_to_detect_crashes:list, tail_lines: int = 100) -> Tuple:
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
        "Exception"
        # Add more error patterns here as necessary
    ]
    ERROR_PATTERNS = ["Worker exiting", "Exception"]  # Add more error patterns as necessary
    crash_logs = []

    # Retrieve all services and pods in the namespace just once
    kubectl_cmd = f"kubectl -n {namespace} get services,pods -o json"
    try:
        response = handle.run_native_cmd(kubectl_cmd)
        services_and_pods = json.loads(response.stdout.strip())["items"]
    except json.JSONDecodeError as json_err:
        print(f"Error parsing JSON response: {str(json_err)}")
        return (True, None)  # Return early if we can't parse the JSON at all
    except Exception as e:
        print(f"Unexpected error while fetching services and pods: {str(e)}")
        return (True, None)

    for service_name_to_check in services_to_detect_crashes:
        service_found = False
        for item in services_and_pods:
            if item.get("kind") == "Service" and item.get("metadata", {}).get("name") == service_name_to_check:
                service_found = True
                pod_labels = item.get('spec', {}).get("selector", None)
                if pod_labels:
                    pod_selector = ",".join([f"{key}={value}" for key, value in pod_labels.items()])
                    try:
                        kubectl_logs_cmd = f"kubectl -n {namespace} logs --selector {pod_selector} --tail={tail_lines}"
                        pod_logs = handle.run_native_cmd(kubectl_logs_cmd).stdout.strip()

                        for error_pattern in ERROR_PATTERNS:
                            if re.search(error_pattern, pod_logs):
                                crash_logs.append({
                                    "service": service_name_to_check,
                                    "pod": item.get('metadata', {}).get('name', 'N/A'),
                                    "namespace": item.get('metadata', {}).get('namespace', 'N/A'),
                                    "error": error_pattern,
                                    "timestamp": re.findall(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", pod_logs)[-1] if re.search(error_pattern, pod_logs) else "Unknown Time"
                                })
                    except Exception as e:
                        # Log the error but don't stop execution
                        print(f"Error fetching logs for service {service_name_to_check}: {str(e)}")
                        pass

        if not service_found:
            print(f"Service {service_name_to_check} not found in namespace {namespace}. Continuing with next service.")

    return (False, crash_logs) if crash_logs else (True, None)
