#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import datetime 
from datetime import timezone
from typing import Tuple
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException

# Constants used in this file
INTERVAL_TO_CHECK = 24  # In hours

class InputSchema(BaseModel):
    namespace: str = Field(
        '',
        description='K8S Namespace',
        title='K8S Namespace'
    )
    threshold: int = Field(
        25,
        description='Restart Threshold Value',
        title='Restart Threshold'
    )

def k8s_get_pods_with_high_restart_printer(output):
    if output is None:
        return

    print(output)

def format_datetime(dt):
    # Format datetime to a string 'YYYY-MM-DD HH:MM:SS UTC'
    return dt.strftime('%Y-%m-%d %H:%M:%S UTC')

def k8s_get_pods_with_high_restart(handle, namespace: str = '', threshold: int = 25) -> Tuple:
    """k8s_get_pods_with_high_restart This function finds out PODS that have
       high restart count and returns them as a list of dictionaries

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :type namespace: str
       :param namespace: K8S Namespace 

       :type threshold: int 
       :param threshold: int Restart Threshold Count value

       :rtype: Tuple Result in tuple format.  
    """
    if handle.client_side_validation is not True:
        raise Exception(f"K8S Connector is invalid {handle}")

    v1 = client.CoreV1Api(api_client=handle)
    
    try:
        pods = v1.list_namespaced_pod(namespace).items if namespace else v1.list_pod_for_all_namespaces().items
        if not pods:
            return (True, None)  # No pods in the namespace
    except ApiException as e:
        raise Exception(f"Error occurred while accessing Kubernetes API: {e}")

    retval = []
    
    # It is not enough to check if the restart count is more than the threshold 
    # we should check if the last time the pod got restarted is not within the 24 hours.
    # If it is, then we need to flag it. If not, it could be that the pod restarted at 
    # some time, but have been stable since then. 

    # Lets take current time and reference time that is 24 hours ago.
    current_time = datetime.datetime.now(timezone.utc)
    interval_time_to_check = current_time - datetime.timedelta(hours=INTERVAL_TO_CHECK)
    interval_time_to_check = interval_time_to_check.replace(tzinfo=timezone.utc)

    for pod in pods:
        for container_status in pod.status.container_statuses or []:
            restart_count = container_status.restart_count
            last_state = container_status.last_state

            if restart_count > threshold:
                if last_state and last_state.terminated:
                    termination_time = last_state.terminated.finished_at
                    termination_time = termination_time.replace(tzinfo=timezone.utc)
                    # We compare if the termination time is within the last 24 hours, if yes
                    # then we need to add it to the retval and return the list back
                    if termination_time and termination_time >= interval_time_to_check:
                        formatted_termination_time = format_datetime(termination_time)
                        formatted_interval_time_to_check = format_datetime(interval_time_to_check)
                        retval.append({"pod": pod.metadata.name, "namespace": pod.metadata.namespace, "termination_time":formatted_termination_time,"interval_time_to_check": formatted_interval_time_to_check})

    return (False, retval) if retval else (True, None)