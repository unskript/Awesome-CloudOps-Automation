##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint

from kubernetes import client
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    pod_name: str = Field(
        title="Pod Name",
        description="K8S Pod Name"
    )
    namespace: str = Field(
        title="Namespace",
        description="K8S Namespace where the POD exists"
    )

def k8s_gather_data_for_pod_troubleshoot_printer(output):
    if not output:
        return
    
    pprint.pprint(output)


def k8s_gather_data_for_pod_troubleshoot(handle, pod_name: str, namespace: str) -> dict:
    """k8s_gather_data_for_pod_troubleshoot This function gathers data from the k8s namespace
       to assist in troubleshooting of a pod. The gathered data are returned in the form of a
       Dictionary with `logs`, `events` and `details` keys. 
       
       :type handle: Object
       :param handle: Object returned from task.validate(...) routine

       :type pod_name: str
       :param pod_name: Name of the K8S POD (Mandatory parameter)

       :type namespace: str 
       :param namespace: Namespace where the above K8S POD is found (Mandatory parameter)

       :rtype: Python Dictionary that has status, logs, events & details as key for the pod
    """
    retval = {}
    if not pod_name or not namespace:
        raise Exception("POD Name and Namespace are mandatory parameters, cannot be None")

    pod_api = client.CoreV1Api(api_client=handle)
    # Gather the Status first
    status = pod_api.read_namespaced_pod_status(name=pod_name, namespace=namespace)
    retval['status'] = status
    
    # Gather Events pertaining to the POD
    pod_events = ''
    events = pod_api.list_namespaced_event(namespace=namespace)
    for event in events.items:
        if event.involved_object.name == pod_name:
            pod_events += event

    retval['events'] = pod_events 

    # Gather Logs pertaining to the POD
    retval['logs'] = pod_api.read_namespaced_pod_log(name=pod_name, namespace=namespace)

    return retval