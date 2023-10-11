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
    namespace: str = Field(..., description='The namespace in which the service resides.', title='Namespace')
    service_name: str = Field(
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
        print("Disk size for the service is within the threshold.")
        return
    else:
        print("ALERT: PVC disk size is below the threshold:")
        print("-" * 40)
        for pvc in pvc_info:
            print(f"PVC: {pvc['pvc_name']} - Utilized: {pvc['used']} of {pvc['capacity']}")
        print("-" * 40)


def k8s_check_service_pvc_utilization(handle, service_name: str, namespace: str, threshold: int=80) -> Tuple:
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
    # Get the labels associated with the service
    get_service_labels_command = f"kubectl get service {service_name} -n {namespace} -o=jsonpath='{{.spec.selector}}'"
    response = handle.run_native_cmd(get_service_labels_command)
    if not response or response.stderr:
        raise ApiException(f"Error while executing command ({get_service_labels_command}): {response.stderr if response else 'empty response'}")

    labels_dict = json.loads(response.stdout.replace("'", "\""))  # Convert to valid JSON format
    label_selector = ",".join([f"{k}={v}" for k, v in labels_dict.items()])

    # Identify a running pod that is utilizing the target PVC using the fetched labels
    get_pod_command = f"kubectl get pods -n {namespace} -l {label_selector} -o=jsonpath='{{.items[0].metadata.name}}'"
    response = handle.run_native_cmd(get_pod_command)
    if not response or response.stderr:
        raise ApiException(f"Error while executing command ({get_pod_command}): {response.stderr if response else 'empty response'}")
    pod_name = response.stdout.strip()
    print(f"Identified pod utilizing the PVC: {pod_name}")

    # Get the PVC names mounted in the identified Pod
    get_pvc_names_command = f"kubectl get pod {pod_name} -n {namespace} -o=jsonpath='{{.spec.volumes[*].persistentVolumeClaim.claimName}}'"
    response = handle.run_native_cmd(get_pvc_names_command)
    if not response or response.stderr:
        raise ApiException(f"Error while executing command ({get_pvc_names_command}): {response.stderr if response else 'empty response'}")

    pvc_names = response.stdout.strip().split()
    print(f"PVCs associated with pod {pod_name} are: {', '.join(pvc_names)}")

    # Check usage for each PVC
    alert_pvcs = []
    for pvc_name in pvc_names:
        # Fetch the complete JSON configuration of the pod
        get_pod_config_command = f"kubectl get pod {pod_name} -n {namespace} -o json"
        response = handle.run_native_cmd(get_pod_config_command)
        if not response or response.stderr:
            raise ApiException(f"Error while executing command ({get_pod_config_command}): {response.stderr if response else 'empty response'}")

        pod_data = json.loads(response.stdout)

        mount_path = ""
        # Traverse the volumes to find our PVC and extract its mount path
        for volume in pod_data["spec"]["volumes"]:
            if "persistentVolumeClaim" in volume and volume["persistentVolumeClaim"]["claimName"] == pvc_name:
                for container in pod_data["spec"]["containers"]:
                    for volume_mount in container["volumeMounts"]:
                        if volume_mount["name"] == volume["name"]:
                            mount_path = volume_mount["mountPath"]
                            break
                if mount_path:
                    break

        print(f"Mount path for PVC inside the pod: {mount_path}")

        # Create a utility pod to calculate the actual space used on the PVC
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
                        "volumeMounts": [
                            {
                                "name": "target-pvc",
                                "mountPath": "/data"
                            }
                        ]
                    }
                ],
                "volumes": [
                    {
                        "name": "target-pvc",
                        "persistentVolumeClaim": {
                            "claimName": pvc_name
                        }
                    }
                ]
            }
        }

        # Deploy the utility pod
        with open("/tmp/utility-pod.yaml", "w") as f:
            json.dump(utility_pod_spec, f)

        apply_command = "kubectl apply -f /tmp/utility-pod.yaml"
        response = handle.run_native_cmd(apply_command)
        if not response or response.stderr:
            raise ApiException(f"Error while applying utility pod spec: {response.stderr if response else 'empty response'}")

        # Wait for the utility pod to be running
        wait_command = "kubectl wait --for=condition=Ready pod/pvc-utility-pod --timeout=60s -n " + namespace
        response = handle.run_native_cmd(wait_command)
        if not response or response.stderr:
            raise ApiException(f"Utility pod did not become ready: {response.stderr if response else 'empty response'}")

        # Execute the `du` command in the utility pod
        du_command = f"kubectl exec -n {namespace} pvc-utility-pod -- du -sh /data"
        du_output = handle.run_native_cmd(du_command)
        if not du_output or du_output.stderr:
            raise ApiException(f"Error while calculating used space: {du_output.stderr if du_output else 'empty response'}")

        # Parse the output to extract size
        used_space = du_output.stdout.split()[0]
        # Convert to GiB
        if used_space[-1] == "G":
            used_space_gib = float(used_space[:-1])
        elif used_space[-1] == "M":
            used_space_gib = float(used_space[:-1]) / 1024
        elif used_space[-1] == "K":
            used_space_gib = float(used_space[:-1]) / (1024 * 1024)
        else:
            raise ValueError("Unexpected unit in du output")

        # Delete the utility pod
        delete_command = "kubectl delete -f /tmp/utility-pod.yaml"
        response = handle.run_native_cmd(delete_command)
        if not response or response.stderr:
            print(f"Warning: Error while deleting utility pod: {response.stderr if response else 'empty response'}")

        # Get the total capacity of the PVC
        get_pvc_capacity_command = f"kubectl get pvc {pvc_name} -n {namespace} -o=jsonpath='{{.status.capacity.storage}}'"
        response = handle.run_native_cmd(get_pvc_capacity_command)
        if not response or response.stderr:
            raise ApiException(f"Error while executing command ({get_pvc_capacity_command}): {response.stderr if response else 'empty response'}")
        total_capacity_str = response.stdout.strip()
        # Extract the number from strings like "10Gi"
        total_capacity_gib = float(re.findall(r"(\d+)", total_capacity_str)[0])

        # Calculate the percentage of used space
        used_percentage = (used_space_gib / total_capacity_gib) * 100
        remaining_percentage = 100 - used_percentage

        print(f"Total PVC capacity for {pvc_name}: {total_capacity_gib:.2f}Gi")
        print(f"Actual used space in PVC {pvc_name}: {used_space_gib:.2f}Gi")
        print(f"Percentage of used space for {pvc_name}: {used_percentage:.2f}%")
        print(f"Remaining space percentage for {pvc_name}: {remaining_percentage:.2f}%")

        if remaining_percentage < threshold:
            alert_pvcs.append({"pvc_name": pvc_name, "namespace": namespace, "used": f"{used_space_gib:.2f}Gi", "capacity": f"{total_capacity_gib:.2f}Gi"})

    if alert_pvcs:
        return (False, alert_pvcs)

    return (True, None)


