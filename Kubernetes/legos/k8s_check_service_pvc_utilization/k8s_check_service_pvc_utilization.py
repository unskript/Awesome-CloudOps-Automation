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
     namespace: str = Field(..., description='The namespace in which the service resides.', title='Namespace')
     services_to_check_pvc_utilzation: list = Field(
         ...,
         description='List of services for which the used PVC size needs to be checked.',
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

def k8s_check_service_pvc_utilization(handle, services_to_check_pvc_utilzation: list, namespace:str, threshold: int = 80) -> Tuple:
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

    alert_pvcs_all_services = []
    services_without_pvcs = []

    for svc in services_to_check_pvc_utilzation:
        # Get label associated with the service
        get_service_labels_command = f"kubectl get services {svc} -n {namespace} -o=jsonpath='{{.spec.selector}}'"
        response = handle.run_native_cmd(get_service_labels_command)
        if not response.stdout.strip():
            # No labels found for a particular service. Skipping...
            continue
        labels_dict = json.loads(response.stdout.replace("'", "\""))
        label_selector = ",".join([f"{k}={v}" for k, v in labels_dict.items()])

        # Fetch the pod attached to this service.
        # The safer option is to try with the * option. Having a specific index like 0 or 1
        # will lead to ApiException. 
        get_pod_command = f"kubectl get pods -n {namespace} -l {label_selector} -o=jsonpath='{{.items[*].metadata.name}}'"
        response = handle.run_native_cmd(get_pod_command)
        if not response or response.stderr:
            raise ApiException(f"Error while executing command ({get_pod_command}): {response.stderr if response else 'empty response'}")

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
            json_path_cmd = "{range .items[*]}{.metadata.name}:{range .spec.volumes[*].persistentVolumeClaim}{.claimName} {end}{\"\\n\"}{end}"
        else:
            json_path_cmd = "{.metadata.name}:{range .spec.volumes[*].persistentVolumeClaim}{.claimName}{end}"

        get_pvc_names_command = f"kubectl get pod {pod_names} -n {namespace} -o=jsonpath='{json_path_cmd}'"


        response = handle.run_native_cmd(get_pvc_names_command)
        if not response or response.stderr:
            raise ApiException(f"Error while executing command ({get_pvc_names_command}): {response.stderr if response else 'empty response'}")
        # Example: ['lightbeam-elasticsearch-master-0:data-lightbeam-elasticsearch-master-0']
        pod_and_pvc_names = response.stdout.strip().split()


        # The pod_and_pvc_names 
        if not pod_and_pvc_names:
            services_without_pvcs.append(svc)
            continue

        pvc_mounts = []
        alert_pvcs = []
        all_pvcs = []
        
        for element in pod_and_pvc_names:
            pod_name, claim_name = element.split(':')
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
            get_pod_json_command = f"kubectl get pod {pod_name} -n {namespace} -o json"
            pod_json_output = handle.run_native_cmd(get_pod_json_command)
            if not pod_json_output or pod_json_output.stderr:
                raise ApiException(f"Error fetching pod json for {pod_name}: {pod_json_output.stderr if pod_json_output else 'empty response'}")
            pod_data = json.loads(pod_json_output.stdout)
    
            # Dictionary .get() method with default value is way of error handling
            for container in pod_data.get('spec', {}).get('containers', {}):
                for mount in container.get('volumeMounts', {}):
                    for volume in pod_data.get('spec', {}).get('volumes', {}):
                        if 'persistentVolumeClaim' in volume and volume.get('name') == mount.get('name'):
                            try:
                                claim_name = volume['persistentVolumeClaim']['claimName']
                                pvc_mounts.append({
                                    "container_name": container['name'],
                                    "mount_path": mount['mountPath'],
                                    "pvc_name": claim_name if claim_name else None
                                })
                            except KeyError as e:
                                # Handle the KeyError (e.g., log the error, skip this iteration, etc.)
                                print(f"KeyError: {e}. Skipping this entry.")
                            except IndexError as e:
                                # Handle the IndexError (e.g., log the error, skip this iteration, etc.)
                                print(f"IndexError: {e}. Skipping this entry.")


        all_mounts = [mount.get('mount_path') for mount in pvc_mounts]
        all_mounts = " ".join(all_mounts).strip()
        for mount in pvc_mounts:
            container_name = mount['container_name']
            mount_path = mount['mount_path']
            pvc_name = mount['pvc_name']
            all_pvcs.append({"pvc_name": pvc_name, "mount_path": mount_path, "used": None, "capacity": None})

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