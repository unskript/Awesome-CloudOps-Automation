#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

from typing import Optional, Tuple
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException
from tabulate import tabulate
import datetime
from datetime import timezone 


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='k8s Namespace')
    time_interval_to_check: int = Field(
        24,
        description='Time interval in hours. This time window is used to check if POD was in Crashloopback. Default is 24 hours.',
        title="Time Interval"
    )


def k8s_get_pods_in_crashloopbackoff_state_printer(output):
    status, data = output

    if status:
        print("No pods are in CrashLoopBackOff state.")
    else:
        headers = ["Pod Name", "Namespace", "Container Name"]
        table_data = [(entry["pod"], entry["namespace"], entry["container"]) for entry in data]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

def format_datetime(dt):
    # Format datetime to a string 'YYYY-MM-DD HH:MM:SS UTC'
    return dt.strftime('%Y-%m-%d %H:%M:%S UTC')

def k8s_get_pods_in_crashloopbackoff_state(handle, namespace: str = '', time_interval_to_check=24) -> Tuple:
    """
    k8s_get_pods_in_crashloopbackoff_state returns the pods that have CrashLoopBackOff state in their container statuses within the specified time interval.

    :type handle: Object
    :param handle: Object returned from the task.validate(...) function

    :type namespace: str
    :param namespace: (Optional) String, K8S Namespace as python string

    :type time_interval_to_check: int
    :param time_interval_to_check: (Optional) Integer, in hours, the interval within which the
            state of the POD should be checked.

    :rtype: Status, List of objects of pods, namespaces, and containers that are in CrashLoopBackOff state
    """
    result = []
    if handle.client_side_validation is not True:
        raise ApiException(f"K8S Connector is invalid {handle}")

    v1 = client.CoreV1Api(api_client=handle)

    try:
        if namespace:
            response = v1.list_namespaced_pod(namespace)
        else:
            response = v1.list_pod_for_all_namespaces()

        if response is None or not hasattr(response, 'items'):
            raise ApiException("Unexpected response from the Kubernetes API. 'items' not found in the response.")

        pods = response.items

    except ApiException as e:
        raise e

    if pods is None:
        raise ApiException("No pods returned from the Kubernetes API.")

    current_time = datetime.datetime.now(timezone.utc)
    interval_time_to_check = current_time - datetime.timedelta(hours=time_interval_to_check)
    interval_time_to_check = interval_time_to_check.replace(tzinfo=timezone.utc)

    for pod in pods:
        pod_name = pod.metadata.name
        namespace = pod.metadata.namespace
        container_statuses = pod.status.container_statuses
        if container_statuses is None:
            continue
        for container_status in container_statuses:
            container_name = container_status.name
            if container_status.state and container_status.state.waiting and container_status.state.waiting.reason == "CrashLoopBackOff":
                # Check if the last transition time to CrashLoopBackOff is within the specified interval
                if container_status.last_state and container_status.last_state.terminated:
                    last_transition_time = container_status.last_state.terminated.finished_at
                    if last_transition_time:
                        last_transition_time = last_transition_time.replace(tzinfo=timezone.utc)
                        if last_transition_time >= interval_time_to_check:
                            formatted_transition_time = format_datetime(last_transition_time)
                            formatted_interval_time_to_check = format_datetime(interval_time_to_check)
                            result.append({
                                "pod": pod_name,
                                "namespace": namespace,
                                "container": container_name,
                                "last_transition_time": formatted_transition_time,
                                "interval_time_to_check": formatted_interval_time_to_check
                            })

    return (False, result) if result else (True, None)
