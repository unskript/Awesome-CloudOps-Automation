#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import os 
import json 

from typing import Optional, Tuple
from pydantic import BaseModel, Field
from tabulate import tabulate



class InputSchema(BaseModel):
    services: list = Field(
        description='List of pod names of the services for which memory utilization is to be fetched.',
        title='List of pod names (as services)',
    )
    namespace: str = Field(
        description='Namespace in which the services are running.',
        title='K8s Namespace',
    )
    threshold: Optional[float] = Field(
        80,
        description='Threshold for memory utilization percentage. Default is 80%.',
        title='Threshold (in %)',
    )
        
    
def k8s_get_memory_utilization_of_services_printer(output):
    status, data = output
    if status:
        print("All services are within memory utilization threshold")
    else:
        headers = ["Service", "Pod", "Namespace", "Container", "Utilization %"]
        table_data = []

        for entry in data:
            service = entry.get('service', "N/A")
            pod = entry.get('pod', "N/A")
            namespace = entry.get('namespace', "N/A")
            container = entry.get('container_name', "N/A")
            utilization_percentage = entry.get('utilization_percentage', "N/A")

            table_data.append([service, pod, namespace, container, utilization_percentage])
        
        # Using tabulate to format the output as a grid table
        print(tabulate(table_data, headers=headers, tablefmt="grid"))


def convert_memory_to_bytes(memory_value) -> int:
    if not memory_value:
        return 0
    units = {
        'K': 1000,
        'M': 1000 * 1000,
        'G': 1000 * 1000 * 1000,
        'T': 1000 * 1000 * 1000 * 1000,
        'Ki': 1024,
        'Mi': 1024 * 1024,
        'Gi': 1024 * 1024 * 1024,
        'Ti': 1024 * 1024 * 1024 * 1024,
    }

    for unit, multiplier in units.items():
        if memory_value.endswith(unit):
            return int(memory_value[:-len(unit)]) * multiplier

    return int(memory_value)

def k8s_get_memory_utilization_of_services(handle, namespace: str = "", threshold:float=80, services: list=[]) -> Tuple:
    """
    k8s_get_memory_utilization_of_services executes the given kubectl commands
    to find the memory utilization of the specified services in a particular namespace
    and compares it with a given threshold.

    :param handle: Object returned from the Task validate method, must have client-side validation enabled.
    :param namespace: Namespace in which the services are running.
    :param threshold: Threshold for memory utilization percentage. Default is 80%.
    :param services: List of pod names of the services for which memory utilization is to be fetched.
    :return: Status, list of exceeding services if any service has exceeded the threshold.
    """
    if handle.client_side_validation is False:
        raise Exception(f"K8S Connector is invalid: {handle}")

    if services and not namespace:
        raise ValueError("Namespace must be provided if services are specified.")

    if not namespace:
        namespace = 'default'

    exceeding_services = []

    # Main Idea:
    # 1. Given namespace, lets get current memory utilization for top pods
    # 2. Filter the list of pods to check from the service list
    # 3. For the pods get the memory request
    # 4. Calculate utilization as (mem_usage / mem_request) * 100
    # 5. Construct list of pods which has  Utilization > threshold  and return the list

    try:

        top_pods_command = f"kubectl top pods -n {namespace} --containers --no-headers"
        response = handle.run_native_cmd(top_pods_command)
        top_pods_output = response.stdout.strip()
        if not top_pods_output:
            return (True, None)
        
        service_pods_containers = {}  # Dictionary to hold pod and container names for each service
        if services:
            # If services specified, lets iterate over it and get pods corresponding to them.
            # If service pod not found in the top pod list, which means the memory
            # utilization is not significant, so dont need to check
            for svc in services:
                kubectl_cmd = f"kubectl get service {svc} -n {namespace} -o=jsonpath={{.spec.selector}}"
                response = handle.run_native_cmd(kubectl_cmd)
                svc_labels = None 
                if response.stderr:
                    print(f"Error occurred while executing command {kubectl_cmd}: {response.stderr}")
                    continue
                try:
                    if response.stdout.strip():
                        svc_labels = json.loads(response.stdout.strip())
                except:
                    # If json.loads returns error, which means the output of the kubectl command returned invalid output.
                    # since there is invalid output, no service label output. the next if check should return back
                    pass 

                if not svc_labels:
                    continue
                _labels = ", ".join([f"{key}={value}" for key, value in svc_labels.items()])
                svc_pod_cmd = f"kubectl get pods -n {namespace} -l \"{_labels}\" -o=jsonpath={{.items[*].metadata.name}}"
                response = handle.run_native_cmd(svc_pod_cmd)
                svc_pods = response.stdout.strip()
                if not svc_pods:
                    # No pods attached to the given service
                    continue

                # For each pod, fetch containers and their memory usage
                for svc_pod in svc_pods.split():
                    for line in top_pods_output.split('\n'):
                        if svc_pod in line:
                            parts = line.split()
                            if len(parts) >= 3:  # Ensure line has enough parts to parse
                                container_name = parts[1]
                                mem_usage = parts[-1]
                            else:
                                print(f"Incorrect top pods output for pod:{svc_pod} namespace: {namespace}.")
                                continue

                            # Key: Service, Pod, Container; Value: Memory Usage
                            service_pods_containers[(svc, svc_pod, container_name)] = mem_usage
        else:
            for line in top_pods_output.split('\n'):
                parts = line.split()
                if len(parts) >= 3:
                    pod_name, container_name, mem_usage = parts[0], parts[1], parts[-1]
                else:
                    print(f"Incorrect top pods output for namespace: {namespace}.")
                    continue

                # Key: Service: None, Pod, Container; Value: Memory Usage (when services are not specified)
                service_pods_containers[(None, pod_name, container_name)] = mem_usage

        # Now, for each service's pod and container, fetch memory request and calculate utilization
        for (service_key, pod, container), mem_usage in service_pods_containers.items():
                # Check if the service name exists or use a placeholder
                service_name = service_key if service_key else "N/A"
                # Kubernetes pod must have at least one container. The container is the smallest deployable unit in 
                # Kubernetes. A pod encapsulates one or more containers, storage resources, a unique network IP, 
                # and options that govern how the container(s) should run. When you define a pod manifest in Kubernetes, 
                # you define one or more containers within it. Each container has its own image, environment variables, 
                # resources, and other configuration settings. It's the containers within the pod that execute the actual application 
                # code or processes. Without at least one container, there would be no workloads running within the pod, and 
                # it would essentially be an empty entity without any purpose in the Kubernetes ecosystem.
                # The below command takes the container name that was obtained earlier and uses it to get the memory request
                kubectl_command = f"kubectl get pod {pod} -n {namespace} -o=jsonpath='{{.spec.containers[?(@.name==\"{container}\")].resources.requests.memory}}'"
                response = handle.run_native_cmd(kubectl_command)
                mem_request = response.stdout.strip()

                if not mem_request:
                     # Memory limit is not set, dont calculate utilization
                    continue

                mem_request_bytes = convert_memory_to_bytes(mem_request)
                mem_usage_bytes = convert_memory_to_bytes(mem_usage)

                if mem_request_bytes > 0:
                    utilization = (mem_usage_bytes / mem_request_bytes) * 100
                    utilization = round(utilization, 2)

                    if utilization > threshold:
                        exceeding_services.append({
                            "service": service_name,
                            "pod": pod,
                            "container_name": container,
                            "namespace": namespace,
                            "utilization_percentage": utilization,
                            "memory_request_bytes": mem_request_bytes,
                            "memory_usage_bytes": mem_usage_bytes,
                        })
                else:
                    print(f"Memory request for pod: {pod}, container: {container} is 0 or not set. Skipping...")
                    continue

    except Exception as e:
        raise e

    return (False, exceeding_services) if exceeding_services else (True, None)