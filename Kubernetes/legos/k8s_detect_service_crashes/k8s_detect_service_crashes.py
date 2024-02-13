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
    try:
        kubectl_cmd = "kubectl "
        if namespace:
            kubectl_cmd += f"-n  {namespace} "
        kubectl_cmd += "get services,pods -o json"
        response = handle.run_native_cmd(kubectl_cmd)
        services_and_pods = {}

        if response:
            response = response.stdout.strip()
            services_and_pods = json.loads(response)["items"]
        for item in services_and_pods:
            if item.get("kind") == "Service":
                pass 
                service_name = item.get("metadata", {}).get("name", None)
                pod_labels = item.get('spec', {}).get("selector", None)
                if pod_labels and service_name:
                    pod_selector = ",".join([f"{key}={value}" for key, value in pod_labels.items()])
                    try:
                        kubectl_logs_cmd = "kubectl "
                        if namespace:
                            kubectl_logs_cmd += f"-n  {namespace}"
                        kubectl_logs_cmd += f"logs --selector  {pod_selector} --tail={tail_lines}"
                        pod_logs = handle.run_native_cmd(kubectl_logs_cmd)
                        pod_logs = pod_logs.stdout.strip()
                        crash_logs = [{
                                "pod": item.get('metadata', {}).get('name', 'N/A'),
                                "namespace": item.get('metadata', {}).get('namespace', 'N/A'),
                                "error": error_pattern,
                                "timestamp": re.findall(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", pod_logs)[-1] if re.search(error_pattern, pod_logs) else "Unknown Time"
                                } for error_pattern in ERROR_PATTERNS if re.search(error_pattern, pod_logs)]
                    except Exception as e:
                        raise e
                    
    except Exception as e:
        raise e
    
    return (False, crash_logs) if crash_logs else (True, None)
