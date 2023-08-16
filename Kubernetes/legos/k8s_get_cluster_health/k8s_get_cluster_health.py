##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from typing import Tuple
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException
from tabulate import tabulate

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
    status, details_list = output
    details = details_list[0]
    
    # Print overall status
    if status:
        print("Cluster Health: OK\n")
        return

    # If there are any issues, tabulate and print them
    print("Cluster Health: NOT OK\n")

    # Print Not Ready Nodes
    if details['not_ready_nodes']:
        headers = ["Name", "Type", "Status", "Reason", "Message"]
        table = [[node['name'], node['condition_type'], node['condition_status'], node['condition_reason'], node['condition_message']] 
                 for node in details['not_ready_nodes']]
        print("Not Ready Nodes:")
        print(tabulate(table, headers=headers, tablefmt='grid', numalign="left"))
        print()

    # Print Not Ready Pods
    if details['not_ready_pods']:
        headers = ["Name", "Namespace", "Type", "Status", "Reason", "Message"]
        table = [[pod['name'], pod['namespace'], pod['condition_type'], pod['condition_status'], pod['condition_reason'], pod['condition_message']] 
                 for pod in details['not_ready_pods']]
        print("Not Ready Pods:")
        print(tabulate(table, headers=headers, tablefmt='grid', numalign="left"))
        print()

    # Print Abnormal Nodes
    if details['abnormal_nodes']:
        headers = ["Name", "Events"]
        table = [[node['name'], node['events']] for node in details['abnormal_nodes']]
        print("Nodes with Abnormal Events:")
        print(tabulate(table, headers=headers, tablefmt='grid', numalign="left"))
        print()



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

    retval = {}
    not_ready_nodes = []
    not_ready_pods = []
    abnormal_nodes = []

    node_api = pods_api = client.CoreV1Api(api_client=handle)
    nodes = node_api.list_node()
    
    for node in nodes.items:
        skip_remaining_checks = False
        # Get Node Status
        conditions = node.status.conditions
        for condition in conditions:
            if condition.type == 'Ready' and condition.status == 'False':
                not_ready_nodes.append({
                    'name': node.metadata.name,
                    'condition_type': condition.type,
                    'condition_status': condition.status,
                    'condition_reason': condition.reason,
                    'condition_message': condition.message
                })
                skip_remaining_checks = True
                break

        # Node is not ready, no need to perform other checks
        if skip_remaining_checks:
            continue

        # Lets get abnormal events. Lets go with `warning` as the default level
        events = k8s_get_abnormal_events(node_api, node.metadata.name)
        if events != '':
            abnormal_nodes.append({'name': node.metadata.name, 'events': events})

    # Check the status of the Kubernetes pods
    pods = pods_api.list_pod_for_all_namespaces()
    for pod in pods.items:
        conditions = pod.status.conditions
        for condition in conditions:
            if condition.type == 'Ready' and condition.status == 'False':
                not_ready_pods.append({
                    'name': pod.metadata.name,
                    'namespace': pod.metadata.namespace,
                    'condition_type': condition.type,
                    'condition_status': condition.status,
                    'condition_reason': condition.reason,
                    'condition_message': condition.message
                })
                break

    # If any of the above checks have failed, raise an exception
    if len(not_ready_nodes) > 0 or len(not_ready_pods) > 0 or len(abnormal_nodes) > 0:
        retval['not_ready_nodes'] = not_ready_nodes
        retval['not_ready_pods'] = not_ready_pods
        retval['abnormal_nodes'] = abnormal_nodes
        return (False, [retval])

    return (True, None)
