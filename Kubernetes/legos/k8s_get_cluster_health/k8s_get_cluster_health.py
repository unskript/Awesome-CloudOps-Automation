##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from typing import Tuple, List
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException

class InputSchema(BaseModel):
    core_services: List= Field(
        default=[],
        title='Core Services',
        description='List of core services names to check for health'
    )

def k8s_get_cluster_health_printer(output):
    status, health_issues = output
    if status:
        print("Cluster Health: OK\n")
    else:
        print("Cluster Health: NOT OK\n")
        for issue in health_issues:
            print(f"Type: {issue['type']}")
            print(f"Name: {issue['name']}")
            print(f"Namespace: {issue.get('namespace', 'N/A')}")
            print(f"Issue: {issue['issue']}")
            print("-" * 40)

def check_node_health(node_api):
    nodes = node_api.list_node()
    for node in nodes.items:
        for condition in node.status.conditions:
            if condition.type == "Ready" and condition.status != "True":
                return False
    return True

def check_pod_health(node_api, core_services: List = None):
    health_issues = []
    pods = node_api.list_pod_for_all_namespaces()
    core_services = core_services or [] 
    for pod in pods.items:
        # If core services are specified, check only those. Otherwise, check all pods.
        if core_services:
            if not any(core_service.lower() in pod.metadata.name.lower() for core_service in core_services):
                continue
        # Check pod health
        if pod.status.phase not in ["Running", "Succeeded"]:
            health_issues.append({
                "type": "Pod",
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "issue": "Pod is not running or succeeded."
            })
    return health_issues


def check_deployment_health(apps_api, core_services: List = []) -> List[dict]:
    health_issues = []
    deployments = apps_api.list_deployment_for_all_namespaces()
    core_services = core_services or [] 
    for deployment in deployments.items:
        # If core services are specified, check only those. Otherwise, check all deployments.
        if core_services:
            if not any(core_service.lower() in deployment.metadata.name.lower() for core_service in core_services):
                continue 
        # Check deployment health
        if deployment.status.replicas != deployment.status.available_replicas:
            health_issues.append({
                "type": "Deployment",
                "name": deployment.metadata.name,
                "namespace": deployment.metadata.namespace,
                "issue": "Deployment has replicas mismatch or is not available/progressing."
            })
    return health_issues


def k8s_get_cluster_health(handle, core_services: List = []) -> Tuple:
    health_issues = []

    node_api = client.CoreV1Api(api_client=handle)
    apps_api = client.AppsV1Api(api_client=handle)

    # 1. Check Node Health
    if not check_node_health(node_api):
        health_issues.append({"type": "Node", "issue": "One or more nodes are not ready."})

    # 2. Check Pod Health across all namespaces
    health_issues.extend(check_pod_health(node_api, core_services))

    # 3. Check Deployment Health
    health_issues.extend(check_deployment_health(apps_api, core_services))

    if health_issues:
        return (False, health_issues)
    else:
        return (True, None)
