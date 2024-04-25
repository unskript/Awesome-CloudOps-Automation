##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import json
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from kubernetes import client

class InputSchema(BaseModel):
    core_services: Optional[list] = Field(
        default=[],
        title="Core Services",
        description="List of core services names to check for health. If empty, checks all services."
    )
    namespace: Optional[str] = Field(
        default="",
        title="Namespace",
        description="Namespace of the core services. If empty, checks all namespaces."
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

def execute_kubectl_command(handle, command: str):
    response = handle.run_native_cmd(command)
    if response.stderr.lower():
        print(f"Warning: {response.stderr}")
        if "not found" in response.stderr.lower():
            return None  # Service not found in the given namespace, skip this service
    if response:
        if response.stdout:
            return response.stdout.strip()
        else:
            print(f"No output for command: {command}")
            return None

def get_namespaces(handle):
    command = "kubectl get ns -o=jsonpath='{.items[*].metadata.name}'"
    namespaces_str = execute_kubectl_command(handle, command)
    if namespaces_str:
        return namespaces_str.split()
    return []

def get_label_selector_for_service(handle, namespace: str, service_name: str):
    command = f"kubectl get svc {service_name} -n {namespace} -o=jsonpath='{{.spec.selector}}'"
    label_selector_json = execute_kubectl_command(handle, command)
    if label_selector_json:
        labels_dict = json.loads(label_selector_json.replace("'", "\""))
        return ",".join([f"{k}={v}" for k, v in labels_dict.items()])
    return ''

def check_node_health(node_api):
    health_issues = []
    nodes = node_api.list_node()
    for node in nodes.items:
        ready_condition = next((condition for condition in node.status.conditions if condition.type == "Ready"), None)
        if not ready_condition or ready_condition.status != "True":
            health_issues.append({
                "type": "Node",
                "name": node.metadata.name,
                "issue": f"Node is not ready. Condition: {ready_condition.type if ready_condition else 'None'}, Status: {ready_condition.status if ready_condition else 'None'}"
            })
    return health_issues

def check_pod_health(handle, core_services, namespace):
        health_issues = []
        namespaces = [namespace] if namespace else get_namespaces(handle)

        for ns in namespaces:
            if core_services:
                for service in core_services:
                    label_selector = get_label_selector_for_service(handle, ns, service)
                    if label_selector:
                        # Get all pods for the service
                        command_pods = f"kubectl get pods -n {ns} -l {label_selector} -o=json"
                        pods_info = execute_kubectl_command(handle, command_pods)
                        if pods_info:
                            pods_data = json.loads(pods_info)
                            total_pods = len(pods_data['items'])
                            running_pods = sum(1 for item in pods_data['items'] if item['status']['phase'] == "Running")

                            # Check if at least 70% of pods are running
                            if total_pods > 0:
                                running_percentage = (running_pods / total_pods) * 100
                                if running_percentage < 70:
                                    health_issues.append({
                                        "type": "Pod",
                                        "name": service,
                                        "namespace": ns,
                                        "issue": f"Insufficient running pods. Only {running_pods} out of {total_pods} are running."
                                    })
                        else:
                            print(f"No pods found for service {service} in namespace {ns}.")
                    else:
                        print(f"No label selector found for service {service} in namespace {ns}. Skipping...")
            else:
                # Check all pods in the namespace if no specific services are given
                command = f"kubectl get pods -n {ns} -o=jsonpath='{{.items[?(@.status.phase!=\"Running\")].metadata.name}}'"
                pods_not_running = execute_kubectl_command(handle, command)
                if pods_not_running:
                    for pod_name in pods_not_running.split():
                        health_issues.append({"type": "Pod", "name": pod_name, "namespace": ns, "issue": "Pod is not running."})

        return health_issues

def check_deployment_health(handle, core_services, namespace):
    health_issues = []
    namespaces = [namespace] if namespace else get_namespaces(handle)

    for ns in namespaces:
        if core_services:
            for service in core_services:
                label_selector = get_label_selector_for_service(handle, ns, service)
                if label_selector:
                    command = f"kubectl get deployments -n {ns} -l {label_selector} -o=jsonpath='{{.items[?(@.status.readyReplicas!=@.status.replicas)].metadata.name}}'"
                    deployments_not_ready = execute_kubectl_command(handle, command)
                    if deployments_not_ready:
                        for deployment_name in deployments_not_ready.split():
                            health_issues.append({"type": "Deployment", "name": deployment_name, "namespace": ns, "issue": "Deployment has replicas mismatch or is not available/progressing."})
                else:
                    print(f"Service {service} not found or has no selectors in namespace {ns}. Skipping...")
        else:
            # Check all deployments in the namespace if no specific services are given
            command = f"kubectl get deployments -n {ns} -o=jsonpath='{{.items[?(@.status.readyReplicas!=@.status.replicas)].metadata.name}}'"
            deployments_not_ready = execute_kubectl_command(handle, command)
            if deployments_not_ready:
                for deployment_name in deployments_not_ready.split():
                    health_issues.append({"type": "Deployment", "name": deployment_name, "namespace": ns, "issue": "Deployment has replicas mismatch or is not available/progressing."})

    return health_issues

def k8s_get_cluster_health(handle, core_services: list = [], namespace: str = "") -> Tuple:
    node_api = client.CoreV1Api(api_client=handle)
    health_issues = check_node_health(node_api) + check_pod_health(handle, core_services, namespace) + check_deployment_health(handle, core_services, namespace)
    if health_issues:
        return (False, health_issues)
    else:
        return (True, None)
