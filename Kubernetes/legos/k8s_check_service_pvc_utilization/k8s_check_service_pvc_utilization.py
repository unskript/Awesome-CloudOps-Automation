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
    namespace: str = Field(
        ...,
        description="The namespace in which the service resides.",
        title="Namespace",
    )
    core_services: list = Field(
        ...,
        description="List of services for which the used PVC size needs to be checked.",
        title="K8s Service name",
    )
    threshold: Optional[int] = Field(
        80,
        description="Percentage threshold for utilized PVC disk size.E.g., a 80% threshold checks if the utilized space exceeds 80% of the total PVC capacity.",
        title="Threshold (in %)",
    )

def k8s_check_service_pvc_utilization(
    handle, core_services: list, namespace: str, threshold: int = 60
) -> Tuple:
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

    :return: Status and dictionary with PVC name and its size information if the PVC's disk size exceeds threshold.
    """

    alert_pvcs_all_services = []
    services_without_pvcs = []
    
    # Keep track of processed PVCs to avoid duplicates
    processed_pvcs = set()

    for svc in core_services:
        # Get label associated with the service
        get_service_labels_command = f"kubectl get services {svc} -n {namespace} -o=jsonpath='{{.spec.selector}}'"
        response = handle.run_native_cmd(get_service_labels_command)
        if not response.stdout.strip():
            # No labels found for a particular service. Skipping...
            continue
        labels_dict = json.loads(response.stdout.replace("'", '"'))
        label_selector = ",".join([f"{k}={v}" for k, v in labels_dict.items()])

        # Fetch the pod attached to this service.
        # The safer option is to try with the * option. Having a specific index like 0 or 1
        # will lead to ApiException.
        get_pod_command = f"kubectl get pods -n {namespace} -l {label_selector} -o=jsonpath='{{.items[*].metadata.name}}'"
        response = handle.run_native_cmd(get_pod_command)
        if not response or response.stderr:
            raise ApiException(
                f"Error while executing command ({get_pod_command}): {response.stderr if response else 'empty response'}"
            )

        # pod_names stores the output from the above kubectl command, which is a list of pod_names separated by space
        pod_names = response.stdout.strip()
        if not pod_names:
            # No pods found for service {svc} in namespace {namespace} with labels {label_selector}
            continue

        # Fetch PVCs attached to the pod
        # The Above kubectl command would return a string that is space separated name(s) of the pod.
        # Given such a string, lets find out if we have one or more than one pod name in the string.
        # If there are more than one pod name in the output, we need to iterate over all items[] array.
        # Else we can directly access the persistentVolumeClaim name
        # Lets also associate the pod_name along with the claim name (PVC Name) in the format of
        # pod_name:pv_claim_name

        if len(pod_names.split()) > 1:
            json_path_cmd = '{range .items[*]}{.metadata.name}:{range .spec.volumes[*].persistentVolumeClaim}{.claimName} {end}{"\\n"}{end}'
        else:
            json_path_cmd = "{.metadata.name}:{range .spec.volumes[*].persistentVolumeClaim}{.claimName}{end}"

        get_pvc_names_command = f"kubectl get pod {pod_names} -n {namespace} -o=jsonpath='{json_path_cmd}'"

        response = handle.run_native_cmd(get_pvc_names_command)
        if not response or response.stderr:
            raise ApiException(
                f"Error while executing command ({get_pvc_names_command}): {response.stderr if response else 'empty response'}"
            )
        # Example: ['lightbeam-elasticsearch-master-0:data-lightbeam-elasticsearch-master-0']
        pod_and_pvc_names = response.stdout.strip().split()

        # The pod_and_pvc_names
        if not pod_and_pvc_names:
            services_without_pvcs.append(svc)
            continue

        pvc_mounts = []
        alert_pvcs = []

        for element in pod_and_pvc_names:
            pod_name, claim_name = element.split(":")
            if not claim_name:
                # Skip if Volume Claim name is empty.
                continue

            # Fetch the Pod JSON
            # We need to get the container name (if any) from the Pod's JSON. This is needed
            # if we want to exec into the POD that is within a container. The JSON data that
            # we obtain is used to fill the pvc_mounts list, which is a list of dictionaries.
            # We use this pvc_mounts to find out the used_space percentage. We compare that with
            # the threshold to flag if the utilization is above threshold.
            # df -kh is the command used to get the disk utilization. This is accurate as we get
            # the disk utilization from the POD directly, rather than checking the resource limit
            # and resource request from the deployment / stateful YAML file.
            get_pod_json_command = (
                f"kubectl get pod {pod_name} -n {namespace} -o json"
            )
            pod_json_output = handle.run_native_cmd(get_pod_json_command)
            if not pod_json_output or pod_json_output.stderr:
                raise ApiException(
                    f"Error fetching pod json for {pod_name}: {pod_json_output.stderr if pod_json_output else 'empty response'}"
                )
            pod_data = json.loads(pod_json_output.stdout)

            # Dictionary .get() method with default value is way of error handling
            for container in pod_data.get("spec", {}).get("containers", {}):
                for mount in container.get("volumeMounts", {}):
                    for volume in pod_data.get("spec", {}).get("volumes", {}):
                        if "persistentVolumeClaim" in volume and volume.get(
                            "name"
                        ) == mount.get("name"):
                            try:
                                claim_name = volume["persistentVolumeClaim"][
                                    "claimName"
                                ]
                                print(f"ClaimName: {claim_name}: MountName: {mount['name']} ContainerName: {container['name']}")
                                
                                # Add mount info if not already added
                                mount_info = {
                                    "container_name": container["name"],
                                    "mount_path": mount["mountPath"],
                                    "pvc_name": claim_name if claim_name else None,
                                    "pod_name": pod_name
                                }
                                
                                # Only add if this specific mount combination hasn't been processed yet
                                mount_key = f"{pod_name}:{container['name']}:{mount['mountPath']}:{claim_name}"
                                if mount_key not in processed_pvcs:
                                    pvc_mounts.append(mount_info)
                                    processed_pvcs.add(mount_key)
                                    
                            except KeyError as e:
                                # Handle the KeyError (e.g., log the error, skip this iteration, etc.)
                                print(f"KeyError: {e}. Skipping this entry.")
                            except IndexError as e:
                                # Handle the IndexError (e.g., log the error, skip this iteration, etc.)
                                print(f"IndexError: {e}. Skipping this entry.")

        # Create a dictionary to store processed PVC info
        pvc_info_dict = {}
            
        # Process each mount separately with a single df command
        for mount in pvc_mounts:
            container_name = mount["container_name"]
            mount_path = mount["mount_path"]
            pvc_name = mount["pvc_name"]
            pod_name = mount["pod_name"]
            
            # Skip if we've already processed this PVC
            if pvc_name in pvc_info_dict:
                continue
                
            du_command = f"kubectl exec -n {namespace} {pod_name} -c {container_name} -- df -kh {mount_path} | grep -v Filesystem"
            du_output = handle.run_native_cmd(du_command)

            if du_output and not du_output.stderr:
                # Process each line of df output separately
                df_lines = du_output.stdout.strip().split("\n")

                for df_line in df_lines:
                    if not df_line.strip():
                        continue

                    # Split line into columns
                    columns = re.split(r"\s+", df_line.strip())

                    # Find the percentage column (contains '%')
                    percent_col = None
                    for i, col in enumerate(columns):
                        if "%" in col:
                            percent_col = i
                            break

                    if percent_col is None or len(columns) < 2:
                        print(f"Warning: Unexpected df output format: {df_line}")
                        continue

                    # Extract percentage and capacity
                    used_percentage = int(columns[percent_col].replace("%", ""))
                    total_capacity = columns[1] if len(columns) > 1 else "Unknown"
                    pvc_info = {
                        "pvc_name": pvc_name,
                        "mount_path": mount_path,
                        "used": used_percentage,
                        "capacity": total_capacity,
                    }
                    
                    # Store in dictionary to prevent duplicates
                    pvc_info_dict[pvc_name] = pvc_info

                    # Check if usage exceeds threshold
                    if used_percentage > threshold:
                        alert_pvcs.append(pvc_info)

        # Add unique alert PVCs to the main list
        for pvc_info in alert_pvcs:
            if pvc_info not in alert_pvcs_all_services:
                alert_pvcs_all_services.append(pvc_info)

    if services_without_pvcs:
        print("Following services do not have any PVCs attached:")
        for service in services_without_pvcs:
            print(f"- {service}")

    if alert_pvcs_all_services:
        print(json.dumps(alert_pvcs_all_services, indent=4))

    return (not bool(alert_pvcs_all_services), alert_pvcs_all_services)
