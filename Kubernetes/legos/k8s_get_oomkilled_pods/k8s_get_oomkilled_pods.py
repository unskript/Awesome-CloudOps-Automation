#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import pprint
import datetime
from datetime import timezone 
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



def k8s_get_oomkilled_pods_printer(output):
    if output is None:
        return
    pprint.pprint(output)
    

def k8s_get_oomkilled_pods(handle, namespace: str = "", time_interval_to_check=24) -> Tuple:
    """k8s_get_oomkilled_pods This function returns the pods that have OOMKilled event in the container last states

    :type handle: Object
    :param handle: Object returned from the task.validate(...) function

    :type namespace: str
    :param namespace: (Optional)String, K8S Namespace as python string

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

    # Get Current Time in UTC
    current_time = datetime.datetime.now(timezone.utc)
    # Get time interval to check (or 24 hour) reference and convert to UTC
    interval_time_to_check = current_time - datetime.timedelta(hours=time_interval_to_check)
    interval_time_to_check = interval_time_to_check.replace(tzinfo=timezone.utc)

    
    for pod in pods:
        pod_name = pod.metadata.name
        namespace = pod.metadata.namespace
        
        # Ensure container_statuses is not None before iterating
        container_statuses = pod.status.container_statuses
        if container_statuses is None:
            continue
        
        # Check each pod for OOMKilled state
        for container_status in container_statuses:
            container_name = container_status.name
            last_state = container_status.last_state
            if last_state and last_state.terminated and last_state.terminated.reason == "OOMKilled":
                termination_time = last_state.terminated.finished_at
                # If termination time is greater than interval_time_to_check meaning
                # the POD has gotten OOMKilled in the last 24 hours, so lets flag it!
                if termination_time and termination_time >= interval_time_to_check:
                    result.append({"pod": pod_name, "namespace": namespace, "container": container_name})
    
    return (False, result) if result else (True, None)

