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

        # Fetch the Pod JSON
        get_pod_json_command = f"kubectl get pod {pod_name} -n {namespace} -o json"
        pod_json_output = handle.run_native_cmd(get_pod_json_command)
        if not pod_json_output or pod_json_output.stderr:
            raise ApiException(f"Error fetching pod json for {pod_name}: {pod_json_output.stderr if pod_json_output else 'empty response'}")
        pod_data = json.loads(pod_json_output.stdout)

        # Process the Pod JSON to find PVC mounts
        pvc_mounts = []
        for container in pod_data['spec']['containers']:
            container_name = container['name']
            for mount in container.get('volumeMounts', []):
                mount_path = mount['mountPath']
                volume_name = mount['name']
                # Match the volume name with PVCs in the Pod spec
                for volume in pod_data['spec']['volumes']:
                    if 'persistentVolumeClaim' in volume and volume['name'] == volume_name:
                        pvc_name = volume['persistentVolumeClaim']['claimName']
                        pvc_mounts.append({"container_name": container_name, "mount_path": mount_path, "pvc_name": pvc_name})
        alert_pvcs = []
        # Iterate over pvc_mounts to calculate used space
        for mount in pvc_mounts:
            container_name = mount['container_name']
            mount_path = mount['mount_path']
            pvc_name = mount['pvc_name']

            # Execute the du command
            du_command = f"kubectl exec -n {namespace} {pod_name} -c {container_name} -- du -sh {mount_path}"
            du_output = handle.run_native_cmd(du_command)
            if not du_output or du_output.stderr:
                print(f"Error while calculating used space for mount path {mount_path} in container {container_name}: {du_output.stderr if du_output else 'empty response'}")
                continue

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
                alert_pvcs.append({"pvc_name": pvc_name, "mount_path": mount_path, "used": used_space, "capacity": total_capacity_str})

        alert_pvcs_all_services.extend(alert_pvcs)
    if services_without_pvcs:
        print("Following services do not have any PVCs attached:")
        for service in services_without_pvcs:
            print(f"- {service}")

    return (not bool(alert_pvcs_all_services), alert_pvcs_all_services)
