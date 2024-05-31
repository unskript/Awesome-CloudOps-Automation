#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import pprint
from datetime import datetime, timedelta, timezone
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        '',
        description='Kubernetes Namespace Where the Service exists',
        title='K8S Namespace',
    )
    time_interval_to_check: int = Field(
        24,
        description='Time interval in hours. This time window is used to check if POD good OOMKilled. Default is 24 hours.',
        title="Time Interval"
    )
    restart_threshold: int = Field(
        10,
        description='The threshold for the number of restarts within the specified time interval. Default is 10 restarts.',
        title='Restart Threshold'
    )



def k8s_get_oomkilled_pods_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def format_datetime(dt):
    # Format datetime to a string 'YYYY-MM-DD HH:MM:SS UTC'
    return dt.strftime('%Y-%m-%d %H:%M:%S UTC')

def fetch_restart_events(v1, pod_name, namespace, time_interval):
    """Fetch restart-related events for a specific pod within the given time interval."""
    current_time = datetime.now(timezone.utc)
    start_time = current_time - timedelta(hours=time_interval)
    field_selector = f"involvedObject.name={pod_name},involvedObject.namespace={namespace}"
    event_list = v1.list_namespaced_event(namespace, field_selector=field_selector)
    restart_events = [
        event for event in event_list.items
        if event.reason in ["BackOff", "CrashLoopBackOff"] and
        event.last_timestamp and
        start_time <= event.last_timestamp.replace(tzinfo=timezone.utc) <= current_time
    ]
    return len(restart_events)
    

def k8s_get_oomkilled_pods(handle, namespace: str = "", time_interval_to_check=24, restart_threshold: int = 10) -> Tuple:
    """k8s_get_oomkilled_pods This function returns the pods that have OOMKilled event in the container last states

    :type handle: Object
    :param handle: Object returned from the task.validate(...) function

    :type namespace: str
    :param namespace: (Optional)String, K8S Namespace as python string

    :type time_interval_to_check: int
    :param time_interval_to_check: (Optional) Integer, in hours, the interval within which the
            state of the POD should be checked.

    :rtype: Status, List of objects of pods, namespaces, and containers that are in OOMKilled state
    """
    result = []

    if handle.client_side_validation is not True:
        raise ApiException(f"K8S Connector is invalid {handle}")

    v1 = client.CoreV1Api(api_client=handle)

    # Check whether a namespace is provided, if not fetch all namespaces
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

    # Check if pods is None or not
    if pods is None:
        raise ApiException("No pods returned from the Kubernetes API.")

    interval_time_to_check = datetime.now(timezone.utc) - timedelta(hours=time_interval_to_check)

    for pod in pods:
        pod_name = pod.metadata.name
        namespace = pod.metadata.namespace
        recent_restarts = fetch_restart_events(v1, pod_name, namespace, time_interval_to_check)
        
        # Ensure container_statuses is not None before iterating
        container_statuses = pod.status.container_statuses
        if container_statuses is None:
            continue
        
        # Check each pod for OOMKilled state
        for container_status in container_statuses:
            container_name = container_status.name
            last_state = container_status.last_state
            if last_state and last_state.terminated and last_state.terminated.reason == "OOMKilled":
                oom_time = last_state.terminated.finished_at
                # If termination time is greater than interval_time_to_check meaning
                # the POD has gotten OOMKilled in the last 24 hours and the number of restarts for 
                # that pod is greater than 10, so lets flag it!
                if oom_time and oom_time.replace(tzinfo=timezone.utc) >= interval_time_to_check:
                    if recent_restarts > restart_threshold:
                        formatted_oom_time = format_datetime(oom_time)
                        result.append({
                            "pod": pod_name,
                            "namespace": namespace,
                            "container": container_name,
                            "termination_time": formatted_oom_time,
                            "restarts": recent_restarts
                        })
    return (False, result) if result else (True, None)