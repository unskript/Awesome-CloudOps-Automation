##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from typing import Tuple
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException

class InputSchema(BaseModel):
    threshold : int = Field(
        80,
        title='Threshold',
        description='CPU & Memory Threshold %age'
    )

def k8s_get_cluster_health_printer(output):
    status, health_issues = output

    # Print the overall health status
    if status:
        print("Cluster Health: OK\n")
        return

    print("Cluster Health: NOT OK\n")

    # Print details of the issues
    for issue in health_issues:
        issue_type = issue.get("type", "Unknown Type")
        name = issue.get("name", "Unknown Name")
        namespace = issue.get("namespace", "N/A")
        reason = issue.get("reason", "No specific reason provided")
        message = issue.get("message", "No detailed message")

        print(f"Type: {issue_type}")
        print(f"Name: {name}")
        if namespace != "N/A":
            print(f"Namespace: {namespace}")
        print(f"Reason: {reason}")
        if message != "No detailed message":
            print(f"Message: {message}")
        print("-" * 40)

def check_node_health(node) -> bool:
    for condition in node.status.conditions:
        if condition.type == "Ready" and condition.status == "True":
            return True
    return False

def check_pod_health(pod) -> bool:
    # Check if the pod is in a Running or Succeeded state
    if pod.status.phase not in ["Running", "Succeeded"]:
        return False
    return True

def check_deployment_health(deployment) -> bool:
    return deployment.status.replicas == deployment.status.available_replicas


def k8s_get_cluster_health(handle, threshold: int = 80) -> Tuple:
    health_issues = []

    node_api = client.CoreV1Api(api_client=handle)
    apps_api = client.AppsV1Api(api_client=handle)

    # 1. Check Node Health
    nodes = node_api.list_node()
    for node in nodes.items:
        if not check_node_health(node):
            health_issues.append({"type": "Node", "name": node.metadata.name, "issue": "Node not ready or under pressure."})

    # 2. Check Pod Health across all namespaces
    pods = node_api.list_pod_for_all_namespaces()
    for pod in pods.items:
        if not check_pod_health(pod):
            health_issues.append({"type": "Pod", "name": pod.metadata.name, "namespace": pod.metadata.namespace, "issue": "Pod not ready."})

    # 3. Check Deployment Health
    deployments = apps_api.list_deployment_for_all_namespaces()
    for deployment in deployments.items:
        if not check_deployment_health(deployment):
            health_issues.append({"type": "Deployment", "name": deployment.metadata.name, "namespace": deployment.metadata.namespace, "issue": "Deployment replicas mismatch."})

    if health_issues:
        return (False, health_issues)
    else:
        return (True, None)
