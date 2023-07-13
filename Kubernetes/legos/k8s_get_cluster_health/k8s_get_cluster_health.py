##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from typing import Tuple
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException

try:
    from unskript.legos.kubernetes.k8s_utils import normalize_cpu, normalize_memory
except Exception:
    pass

class InputSchema(BaseModel):
    threshold : int = Field(
        80,
        title='Threshold',
        description='CPU & Memory Threshold %age'
    )

def k8s_get_cluster_health_printer(output):
    if not output:
        return
    print(output)


def k8s_get_abnormal_events(node_api, node_name: str, security_level: str = "Warning") -> str:
    """k8s_get_abnormal_events This is a helper function that is called by the main function to
       get abnormal events with a filter. Default filter (security_level) is set to Warning
    """
    field_selector = f"involvedObject.kind=Node,involvedObject.name={node_name},type={security_level}"
    event_string = ''
    try:
        events = node_api.list_event_for_all_namespaces(field_selector=field_selector)

        # Print the details of each event
        for event in events.items:
            event_string = event_string + f"Event: {event.metadata.name} - {event.type} - \
                {event.reason} - {event.message} - {event.last_timestamp}" + '\n'

    except ApiException as e:
        raise e

    return event_string

def k8s_get_cluster_health(handle, threshold:int = 80) -> Tuple:
    """k8s_get_cluster_health This function takes the Handle as an input parameter,
       finds out all the Nodes present in the Cluster, Finds out the following
       * Any abnormal events seen on the node
       * If the node is under pressure
       * Node Status & Pod Status

       :type handle: object
       :param handle: Object returned from task.validator(...)

       :type threshold: int
       :param threshold: CPU and Memory Threshold 

       :rtype: Tuple
       :param: Tuple that contains result and any errors   
    """
    node_api = pods_api = client.CoreV1Api(api_client=handle)

    nodes = node_api.list_node()
    retval = {}
    for node in nodes.items:
        # Lets check Node Pressure, more than 80%, will need to to raise an exception
        cpu_usage = normalize_cpu(node.status.allocatable['cpu'])
        cpu_capacity = normalize_cpu(node.status.capacity['cpu'])
        mem_usage = normalize_memory(node.status.allocatable['memory'])
        mem_capacity = normalize_memory(node.status.capacity['memory'])
        cpu_usage_percent = (cpu_usage / cpu_capacity) * 100
        mem_usage_percent = (mem_usage / mem_capacity) * 100
        #check if either is over trheshold. If so, add the node and failure to the return value
        if (cpu_usage_percent >= threshold) or (mem_usage_percent >= threshold):
            retval[node.metadata.name] = {}
            if cpu_usage_percent >= threshold:
                retval[node.metadata.name]['cpu_high'] = True
            if mem_usage_percent >= threshold:
                retval[node.metadata.name]['mem_high'] = True

        # Lets get abnormal events. Lets go with `warning` as the default level
        events = k8s_get_abnormal_events(node_api, node.metadata.name)
        if events != '':
            retval['events'] = events

        # Get Node & Pod Condition
        conditions = node.status.conditions
        for condition in conditions:

            if condition.type == 'Ready' and condition.status == 'True':
                retval['not_ready'] = False
                break
            retval['not_ready'] = True
            retval['node_condition'] = condition


        # Check the status of the Kubernetes pods
        pods = pods_api.list_pod_for_all_namespaces()
        retval['not_ready_pods'] = {}
        for pod in pods.items:
            conditions = pod.status.conditions
            for condition in conditions:
                if condition.type == 'Ready' and condition.status == 'True':
                    break
                else:
                    retval['not_ready_pods'].update({
                        'name': pod.metadata.name,
                        'namespace': pod.metadata.namespace
                        })

    if retval:
        return (False, [retval])

    return (True, [])
