#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from kubernetes.client.rest import ApiException
import re
import json


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(..., description='The namespace in which the service resides.', title='Namespace')
    service_name: Optional[str] = Field(
        ...,
        description='The name of the service for which the used PVC size needs to be checked.',
        title='K8s Sservice name',
    )
    threshold: Optional[int] = Field(
        80,
        description='Percentage threshold for utilized PVC disk size.E.g., a 80% threshold checks if the utilized space exceeds 80% of the total PVC capacity.',
        title='Threshold (in %)',
    )


def k8s_check_service_pvc_utilization_printer(output):
    status, pvc_info = output

    if status:
        print("Disk sizes for all checked services are within the threshold.")
    else:
        print("ALERT: One or more PVC disk sizes are below the threshold:")
        print("-" * 40)
        for pvc in pvc_info:
            print(f"PVC: {pvc['pvc_name']} - Utilized: {pvc['used']} of {pvc['capacity']}")
        print("-" * 40)


def k8s_check_service_pvc_utilizationk8s_check_service_pvc_utilization(handle, service_name: str = "", namespace: str = "", threshold: int = 80) -> Tuple:
    """
    k8s_check_service_pvc_utilization checks the utilized disk size of a service's PVC against a given threshold.

    This function fetches the PVC associated with a given service, determines its utilized size,
    and then compares it to its total capacity. If the used percentage exceeds the provided threshold,
    it triggers an alert.

    :type handle: object
    :param handle: Handle object to execute the kubectl command.

    :type service_name: str
    :param service_name: The name of the service.

    :type threshold: int
    :param threshold: Percentage threshold for utilized PVC disk size.
                      E.g., a 80% threshold checks if the utilized space exceeds 80% of the total PVC capacity.

    :type namespace: str
    :param namespace: The namespace in which the service resides.

    :return: Status and dictionary with PVC name and its size information if the PVC's disk size is below the threshold.
    """
    # Fetch namespace based on service name
    if service_name and not namespace:
        get_service_namespace_command = f"kubectl get service {service_name} -o=jsonpath='{{.metadata.namespace}}'"
        response = handle.run_native_cmd(get_service_namespace_command)
        if not response or response.stderr:
            raise ApiException(f"Error fetching namespace for service {service_name}: {response.stderr if response else 'empty response'}")
        namespace = response.stdout.strip()
        print(f"Service {service_name} belongs to namespace: {namespace}")

    # Get current context's namespace if not provided
    if not namespace:
        get_ns_command = "kubectl config view --minify --output 'jsonpath={..namespace}'"
        response = handle.run_native_cmd(get_ns_command)
        if not response or response.stderr:
            raise ApiException(f"Error fetching current namespace: {response.stderr if response else 'empty response'}")
        namespace = response.stdout.strip() or "default"
        print(f"Operating in the current namespace: {namespace}")

    # Get all services in the namespace if service_name is not specified
    services_to_check = [service_name] if service_name else []
    if not service_name:
        get_all_services_command = f"kubectl get svc -n {namespace} -o=jsonpath='{{.items[*].metadata.name}}'"
        response = handle.run_native_cmd(get_all_services_command)
        if not response or response.stderr:
            raise ApiException(f"Error fetching services in namespace {namespace}: {response.stderr if response else 'empty response'}")
        services_to_check = response.stdout.strip().split()

    utility_pod_created = False
    alert_pvcs_all_services = []
    services_without_pvcs = []

    for svc in services_to_check:

        # Get service's pod based on its labels
        get_service_labels_command = f"kubectl get service {svc} -n {namespace} -o=jsonpath='{{.spec.selector}}'"
        response = handle.run_native_cmd(get_service_labels_command)
        if not response.stdout.strip():
            # No labels found for a particular service. Skipping... 
            continue
        labels_dict = json.loads(response.stdout.replace("'", "\""))
        label_selector = ",".join([f"{k}={v}" for k, v in labels_dict.items()])

        # Fetch the pod attached to this service
        get_pod_command = f"kubectl get pods -n {namespace} -l {label_selector} -o=jsonpath='{{.items[0].metadata.name}}'"
        response = handle.run_native_cmd(get_pod_command)
        if not response or response.stderr:
            raise ApiException(f"Error while executing command ({get_pod_command}): {response.stderr if response else 'empty response'}")
        pod_name = response.stdout.strip()

        # Fetch PVCs attached to the pod
        get_pvc_names_command = f"kubectl get pod {pod_name} -n {namespace} -o=jsonpath='{{.spec.volumes[*].persistentVolumeClaim.claimName}}'"
        response = handle.run_native_cmd(get_pvc_names_command)
        if not response or response.stderr:
            raise ApiException(f"Error while executing command ({get_pvc_names_command}): {response.stderr if response else 'empty response'}")
        pvc_names = response.stdout.strip().split()

        # If there are no PVCs for this service, continue to the next one
        if not pvc_names:
            services_without_pvcs.append(svc)
            continue
        if not utility_pod_created:
            utility_pod_created = True 
            print(f"Creating utility pod to check {len(pvc_names)} PVC(s) for service {service_name}")

            utility_pod_spec = {
                "apiVersion": "v1",
                "kind": "Pod",
                "metadata": {
                    "name": "pvc-utility-pod",
                    "namespace": namespace
                },
                "spec": {
                    "containers": [
                        {
                            "name": "util-container",
                            "image": "busybox:latest",
                            "command": ["/bin/sh", "-c", "sleep 3600"],
                            "volumeMounts": [{"name": f"volume-{idx}", "mountPath": f"/data-{idx}"} for idx, _ in enumerate(pvc_names)]
                        }
                    ],
                    "volumes": [{"name": f"volume-{idx}", "persistentVolumeClaim": {"claimName": name}} for idx, name in enumerate(pvc_names)]
                }
            }

            with open("/tmp/utility-pod.yaml", "w") as f:
                json.dump(utility_pod_spec, f)
            apply_command = "kubectl apply -f /tmp/utility-pod.yaml"
            response = handle.run_native_cmd(apply_command)
            if not response or response.stderr:
                raise ApiException(f"Error while applying utility pod spec: {response.stderr if response else 'empty response'}")
            wait_command = "kubectl wait --for=condition=Ready pod/pvc-utility-pod --timeout=60s -n " + namespace
            response = handle.run_native_cmd(wait_command)
            if not response or response.stderr:
                raise ApiException(f"Utility pod did not become ready: {response.stderr if response else 'empty response'}")

            alert_pvcs = []
            for idx, pvc_name in enumerate(pvc_names):
                du_command = f"kubectl exec -n {namespace} pvc-utility-pod -- du -sh /data-{idx}"
                du_output = handle.run_native_cmd(du_command)
                if not du_output or du_output.stderr:
                    raise ApiException(f"Error while calculating used space for {pvc_name}: {du_output.stderr if du_output else 'empty response'}")
                used_space = du_output.stdout.split()[0]
                if used_space[-1] == "G":
                    used_space_gib = float(used_space[:-1])
                elif used_space[-1] == "M":
                    used_space_gib = float(used_space[:-1]) / 1024
                elif used_space[-1] == "K":
                    used_space_gib = float(used_space[:-1]) / (1024 * 1024)
                else:
                    raise ValueError("Unexpected unit in du output")
                get_pvc_capacity_command = f"kubectl get pvc {pvc_name} -n {namespace} -o=jsonpath='{{.status.capacity.storage}}'"
                response = handle.run_native_cmd(get_pvc_capacity_command)
                if not response or response.stderr:
                    raise ApiException(f"Error while executing command ({get_pvc_capacity_command}): {response.stderr if response else 'empty response'}")
                total_capacity_str = response.stdout.strip()
                total_capacity_gib = float(re.findall(r"(\d+)", total_capacity_str)[0])
                used_percentage = (used_space_gib / total_capacity_gib) * 100
                if used_percentage > threshold:
                    alert_pvcs.append({"pvc_name": pvc_name, "used": used_space, "capacity": total_capacity_str})
            alert_pvcs_all_services.extend(alert_pvcs)
    if utility_pod_created:
        print("Deleting utility pod...")
        delete_command = "kubectl delete -f /tmp/utility-pod.yaml"
        handle.run_native_cmd(delete_command)
    # Print out services without PVCs
    if services_without_pvcs:
        print("Following services do not have any PVCs attached:")
        for service in services_without_pvcs:
            print(f"- {service}")

    return (not bool(alert_pvcs_all_services), alert_pvcs_all_services)