##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException

class InputSchema(BaseModel):
    core_services: Optional[list]= Field(
        default=[],
        title='Core Services',
        description='List of core services names to check for health'
    )
    namespace: Optional[str] = Field(
        "",
        title='Namespace',
        description='Namespace of the core services'
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

def check_pod_health(node_api, core_services, namespace):
    
    health_issues = []
    try:
        if namespace:
            pods = node_api.list_namespaced_pod(namespace)
            if not pods:
                return (True, None)
        else:
            pods = node_api.list_pod_for_all_namespaces()
            print("COLLECTED PODS:\n", pods)
        
        for pod in pods.items:
            labels = pod.metadata.labels or {}
            app_label = labels.get('app', '').lower()
            if core_services and not any(service.lower() in app_label for service in core_services):
                    continue
            if pod.status.phase not in ["Running", "Succeeded"]:
                health_issues.append({
                    "type": "Pod",
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "issue": "Pod is not running or succeeded."
                })
        
        return health_issues
    except ApiException as e:
        print(f"API exception when checking pod health: {e}")
        return []


def check_deployment_health(apps_api, core_services, namespace):
    health_issues = []
    try:
        if namespace:
            deployments = apps_api.list_namespaced_deployment(namespace)
            if not deployments:
                    return (True, None)
        else:
            deployments = apps_api.list_deployment_for_all_namespaces()
            print("COLLECTED DEPS:\n", deployments)
        
        for deployment in deployments.items:
            # Check if labels exist, if not, set app_label to an empty string
            labels = deployment.metadata.labels or {}
            app_label = labels.get('app', '').lower()
            if core_services and not any(service.lower() in app_label for service in core_services):
                    continue
            if deployment.status.replicas != deployment.status.available_replicas:
                health_issues.append({
                    "type": "Deployment",
                    "name": deployment.metadata.name,
                    "namespace": deployment.metadata.namespace,
                    "issue": "Deployment has replicas mismatch or is not available/progressing."
                })
        return health_issues
    except ApiException as e:
        print(f"API exception when checking deployment health: {e}")
        return []


def k8s_get_cluster_health(handle, core_services: list = [], namespace="") -> Tuple:
    health_issues = []

    node_api = client.CoreV1Api(api_client=handle)
    apps_api = client.AppsV1Api(api_client=handle)

    if core_services and not namespace:
        raise ValueError("Namespace must be specified when core services are given.")

    # 1. Check Node Health
    if not check_node_health(node_api):
        health_issues.append({"type": "Node", "issue": "One or more nodes are not ready."})

    # 2. Check Pod Health across all namespaces
    health_issues.extend(check_pod_health(node_api, core_services, namespace))

    # 3. Check Deployment Health
    health_issues.extend(check_deployment_health(apps_api, core_services, namespace))

    if health_issues:
        return (False, health_issues)
    else:
        return (True, None)
