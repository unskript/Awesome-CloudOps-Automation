##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import re

from typing import Optional, List, Tuple
from kubernetes import client
from kubernetes.client.rest import ApiException
from pydantic import BaseModel, Field
from tabulate import tabulate


class InputSchema(BaseModel):
    pass

def k8s_get_cluster_health_printer(output):
    if not output:
        return
    print(output)
    
def normalize_cpu(value):
    """
    Return CPU in milicores if it is configured with value
    """
    if re.match(r"[0-9]{1,9}m", str(value)):
      cpu = re.sub("[^0-9]", "", value)
    elif re.match(r"[0-9]{1,4}$", str(value)):
      cpu = int(value) * 1000
    elif re.match(r"[0-9]{1,15}n", str(value)):
      cpu = int(re.sub("[^0-9]", "", value)) // 1000000
    elif re.match(r"[0-9]{1,15}u", str(value)):
      cpu = int(re.sub("[^0-9]", "", value)) // 1000
    return int(cpu)

def normalize_memory(value):
    """
    Return Memory in MB
    """
    if re.match(r"[0-9]{1,9}Mi?", str(value)):
      mem = re.sub("[^0-9]", "", value)
    elif re.match(r"[0-9]{1,9}Ki?", str(value)):
      mem = re.sub("[^0-9]", "", value)
      mem = int(mem) // 1024
    elif re.match(r"[0-9]{1,9}Gi?", str(value)):
      mem = re.sub("[^0-9]", "", value)
      mem = int(mem) * 1024
    return int(mem)


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
            event_string = event_string + f"Event: {event.metadata.name} - {event.type} - {event.reason} - {event.message} - {event.last_timestamp}" + '\n'
        
    except ApiException as e:
        raise e 

    return event_string

def k8s_get_cluster_health(handle) -> Tuple:
    """k8s_get_cluster_health This function takes the Handle as an input parameter,
       finds out all the Nodes present in the Cluster, Finds out the following
       * Any abnormal events seen on the node
       * If the node is under pressure
       * Node Status & Pod Status

       :type handle: object
       :param handle: Object returned from task.validator(...)

       :rtype: Tuple
       :param: Tuple that contains result and any errors   
    """
    node_api = pods_api = client.CoreV1Api(api_client=handle)

    nodes = node_api.list_node() 
    for node in nodes.items():
        # Lets check Node Pressure, more than 80%, will need to to raise an exception
        cpu_usage = normalize_cpu(node.status.allocatable['cpu'])
        cpu_capacity = normalize_cpu(node.status.capacity['cpu'])
        mem_usage = normalize_memory(node.status.allocatable['memory'])
        mem_capacity = normalize_memory(node.status.capacity['memory'])
        cpu_usage_percent = (cpu_usage / cpu_capacity) * 100
        mem_usage_percent = (mem_usage / mem_capacity) * 100 
        if cpu_usage_percent >= 80 or mem_usage_percent >= 80:
            print(f"Node {node.metadata.name} Experiencing High CPU {round(cpu_usage_percent,2)}% / MEM {round(mem_usage_percent,2)}% usage")
            return (False, [node])

        # Lets get abnormal events. Lets go with `warning` as the default level
        events = k8s_get_abnormal_events(node_api, node.metadata.name)
        if events != '':
            return (False, [{"error": events}])
        
        # Get Node & Pod Condition
        node_condition = []
        conditions = node.status.conditions
        for condition in conditions:
            
            if condition.type == 'Ready' and condition.status == 'True':
                break
            else:
                node_condition.append(condition)
        
        if not node_condition:
            return (False, [{"node_condition": node_condition}])

        # Check the status of the Kubernetes pods
        pods = pods_api.list_pod_for_all_namespaces()
        pod_condition = []
        for pod in pods.items:
            conditions = pod.status.conditions
            for condition in conditions:
                if condition.type == 'Ready' and condition.status == 'True':
                    break
            else:
                pod_condition.append(condition)
        
        if not pod_condition:
            return (False, [{"unhealthy_pods": pod_condition}])
    
    return (True, []) 