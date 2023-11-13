##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import json
from typing import Tuple
from pydantic import BaseModel, Field
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



def k8s_get_cluster_health(handle, threshold: int = 80) -> Tuple:
    """k8s_get_cluster_health This function takes the Handle as an input parameter,
       finds out all the Nodes present in the Cluster, Finds out the following
       * Any abnormal events seen on the node
       * If the node is under pressure
       * Node Status & Pod Status

       :type handle: object
       :param handle: Object returned from task.validate(...) method

       :type threshold: int
       :param threshold: CPU and Memory Threshold

       :rtype: Tuple
       :param: Tuple that contains result and any errors
    """
    retval = {}
    not_ready_nodes = []
    not_ready_pods = []
    abnormal_nodes = []

    # Get node information
    get_nodes_command = "kubectl get nodes -o=json"
    try:
        response = handle.run_native_cmd(get_nodes_command)
        nodes_info = json.loads(response.stdout)
    except Exception as e:
        raise Exception(f"Error fetching node information: {e.stderr}") from e

    for node_info in nodes_info['items']:
        node_name = node_info['metadata']['name']
        skip_remaining_checks = False

        # Get Node Status
        conditions = node_info['status']['conditions']
        for condition in conditions:
            if condition['type'] == 'Ready' and condition['status'] == 'False':
                not_ready_nodes.append({
                    'name': node_name,
                    'condition_type': condition['type'],
                    'condition_status': condition['status'],
                    'condition_reason': condition.get('reason', ''),
                    'condition_message': condition.get('message', '')
                })
                skip_remaining_checks = True
                break

        # Node is not ready, no need to perform other checks
        if skip_remaining_checks:
            continue

        # Get abnormal events for the node
        get_node_events_command = f"kubectl get events --field-selector involvedObject.name={node_name} --all-namespaces -o=json"
        try:
            response = handle.run_native_cmd(get_node_events_command)
            events_info = json.loads(response.stdout)
            events = [event for event in events_info['items'] if event['type'] == 'Warning']
            if events:
                abnormal_nodes.append({'name': node_name, 'events': events})
        except Exception as e:
            print(f"Error fetching events for node {node_name}: {e.stderr}")

    # Check the status of the Kubernetes pods
    get_pods_command = "kubectl get pods --all-namespaces -o=json"
    try:
        response = handle.run_native_cmd(get_pods_command)
        pods_info = json.loads(response.stdout)
    except Exception as e:
        raise Exception(f"Error fetching pod information: {e.stderr}") from e

    for pod_info in pods_info['items']:
        # Skip completed one-time jobs
        if pod_info['status']['phase'] == 'Succeeded':
            continue

        conditions = pod_info['status']['conditions']
        for condition in conditions:
            if condition['type'] == 'Ready' and condition['status'] == 'False':
                not_ready_pods.append({
                    'name': pod_info['metadata']['name'],
                    'namespace': pod_info['metadata']['namespace'],
                    'condition_type': condition['type'],
                    'condition_status': condition['status'],
                    'condition_reason': condition.get('reason', ''),
                    'condition_message': condition.get('message', '')
                })
                break

    # If any of the above checks have failed, raise an exception
    if len(not_ready_nodes) > 0 or len(not_ready_pods) > 0 or len(abnormal_nodes) > 0:
        retval['not_ready_nodes'] = not_ready_nodes
        retval['not_ready_pods'] = not_ready_pods
        retval['abnormal_nodes'] = abnormal_nodes
        return (False, [retval])

    return (True, None)
