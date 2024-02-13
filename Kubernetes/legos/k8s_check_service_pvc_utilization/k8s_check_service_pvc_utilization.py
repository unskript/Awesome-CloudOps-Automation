#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import re
import json
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from kubernetes.client.rest import ApiException

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

def k8s_check_service_pvc_utilization(handle, service_name: str = "", namespace: str = "", threshold: int = 80) -> Tuple:
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

    alert_pvcs_all_services = []
    services_without_pvcs = []

    for svc in services_to_check:
        # Get label associated with the service
        get_service_labels_command = f"kubectl get services {svc} -n {namespace} -o=jsonpath='{{.spec.selector}}'"
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
        if not pod_name:
            print(f"No pods found for service {svc} in namespace {namespace} with labels {label_selector}")
            continue
        
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

        # Fetch the Pod JSON
        get_pod_json_command = f"kubectl get pod {pod_name} -n {namespace} -o json"
        pod_json_output = handle.run_native_cmd(get_pod_json_command)
        if not pod_json_output or pod_json_output.stderr:
            raise ApiException(f"Error fetching pod json for {pod_name}: {pod_json_output.stderr if pod_json_output else 'empty response'}")
        pod_data = json.loads(pod_json_output.stdout)

        pvc_mounts = [
            {"container_name": container['name'],
            "mount_path": mount['mountPath'],
            "pvc_name": volume['persistentVolumeClaim']['claimName']}
            for container in pod_data['spec']['containers']
            for mount in container.get('volumeMounts', [])
            for volume in pod_data['spec']['volumes']
            if 'persistentVolumeClaim' in volume and volume['name'] == mount['name']
        ]

        alert_pvcs = []
        all_pvcs = []

        for mount in pvc_mounts:
            container_name = mount['container_name']
            mount_path = mount['mount_path']
            pvc_name = mount['pvc_name']
            all_pvcs.append({"pvc_name": pvc_name, "mount_path": mount_path, "used": None, "capacity": None})

        all_mounts = [mount.get('mount_path') for mount in pvc_mounts]
        all_mounts = " ".join(all_mounts).strip()
        du_command = f"kubectl exec -n {namespace} {pod_name} -c {container_name} -- df -kh {all_mounts} | grep -v Filesystem"
        du_output = handle.run_native_cmd(du_command)


        if du_output and not du_output.stderr:
            used_space = du_output.stdout.strip()
            for idx, space in enumerate([used_space]):
                space = space.split()
                used_percentage = int(space[-2].replace('%', ''))
                total_capacity_str = space[1].replace('%', '')
                all_pvcs[idx]["used"] = used_percentage
                all_pvcs[idx]["capacity"] =  total_capacity_str
                if used_percentage > threshold:
                    alert_pvcs.append(all_pvcs[idx])

        alert_pvcs_all_services.extend(alert_pvcs)
    if services_without_pvcs:
        print("Following services do not have any PVCs attached:")
        for service in services_without_pvcs:
            print(f"- {service}")

    return (not bool(alert_pvcs_all_services), alert_pvcs_all_services)
