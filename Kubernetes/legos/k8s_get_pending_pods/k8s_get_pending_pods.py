#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Optional, Tuple
from pydantic import BaseModel, Field
import json
from tabulate import tabulate
from datetime import datetime, timedelta, timezone


class InputSchema(BaseModel):
    namespace: Optional[str] = Field('', description='k8s Namespace', title='Namespace')
    time_interval_to_check: int = Field(
        24,
        description='Time interval in hours. This time window is used to check if POD was in Pending state. Default is 24 hours.',
        title="Time Interval"
    )



def k8s_get_pending_pods_printer(output):
    status, data = output

    if status:
        print("There are no pending pods.")
        return
    else:
        headers = ["Pod Name", "Namespace"]
        print(tabulate(data, headers=headers, tablefmt="grid"))


def format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S %Z")

def k8s_get_pending_pods(handle, namespace: str = "", time_interval_to_check=24) -> Tuple:
    """
    k8s_get_pending_pods checks if any pod in the Kubernetes cluster is in 'Pending' status within the specified time interval.

    :type handle: object
    :param handle: Object returned from the Task validate method

    :type namespace: string
    :param namespace: Namespace in which to look for the resources. If not provided, all namespaces are considered

    :type time_interval_to_check: int
    :param time_interval_to_check: (Optional) Integer, in hours, the interval within which the
            state of the POD should be checked.

    :rtype: tuple
    :return: Status, list of pending pods with their namespace and the time they became pending
    """
    if handle.client_side_validation is not True:
        print(f"K8S Connector is invalid: {handle}")
        return False, "Invalid Handle"

    namespace_option = f"--namespace={namespace}" if namespace else "--all-namespaces"

    # Getting pods details in json format
    cmd = f"kubectl get pods -o json {namespace_option}"
    result = handle.run_native_cmd(cmd)

    if result.stderr:
        raise Exception(f"Error occurred while executing command {cmd}: {result.stderr}")

    pods = json.loads(result.stdout)['items']
    pending_pods = []

    current_time = datetime.now(timezone.utc)
    interval_time_to_check = current_time - timedelta(hours=time_interval_to_check)
    interval_time_to_check = interval_time_to_check.replace(tzinfo=timezone.utc)

    for pod in pods:
        name = pod['metadata']['name']
        status = pod['status']['phase']
        pod_namespace = pod['metadata']['namespace']

        if status == 'Pending':
            # Check if the pod has been in Pending state within the specified the last 24 hours
            start_time = pod['status'].get('startTime')
            if start_time:
                start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                if start_time >= interval_time_to_check:
                    formatted_start_time = format_datetime(start_time)
                    formatted_interval_time_to_check = format_datetime(interval_time_to_check)
                    pending_pods.append({
                        "pod": name,
                        "namespace": pod_namespace,
                        "start_time": formatted_start_time,
                        "interval_time_to_check": formatted_interval_time_to_check
                    })

    if pending_pods:
        return (False, pending_pods)
    return (True, None)
