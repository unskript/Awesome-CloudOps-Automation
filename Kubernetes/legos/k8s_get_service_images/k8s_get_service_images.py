#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Optional, Dict
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException
from tabulate import tabulate 
import json

class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        '',
        description='K8S Namespace',
        title='K8S Namespace'
    )


def k8s_get_service_images_printer(output):
    table_data = []
    if len(output) == 0:
        print("No data available")
        return
    for service, images in output.items():
        shortened_images = [image for image in images]
        if not shortened_images:
            table_data.append([service, "No images found"])
        else:
            # Join multiple shortened images into a single string
            table_data.append([service, "\n".join(shortened_images)])

    headers = ["Service (Namespace)", "Images"]
    table = tabulate(table_data, headers=headers, tablefmt='grid')
    print(table)



def k8s_get_service_images(handle, namespace:str = "") -> Dict:
    """
    k8s_get_service_images collects the images of running services in the provided namespace.

    :type handle: Object
    :param handle: Object returned from the task.validate(...) function

    :type namespace: str, optional
    :param namespace: The namespace in which the services reside. If not provided, images from all namespaces are fetched.

    :return: Dictionary with service names as keys and lists of image names as values.
    """

    if not namespace:
        get_namespaces_command = "kubectl get ns -o=jsonpath='{.items[*].metadata.name}'"
        response = handle.run_native_cmd(get_namespaces_command)
        if not response or response.stderr:
            raise ApiException(f"Error while executing command ({get_namespaces_command}): {response.stderr if response else 'empty response'}")
        namespaces = response.stdout.strip().split()
    else:
        namespaces = [namespace]

    service_images = {}

    for ns in namespaces:
        # Get the names of all services in the namespace
        get_services_command = f"kubectl get svc -n {ns} -o=jsonpath='{{.items[*].metadata.name}}'"
        response = handle.run_native_cmd(get_services_command)
        if not response or response.stderr:
            raise ApiException(f"Error while executing command ({get_services_command}): {response.stderr if response else 'empty response'}")

        service_names = response.stdout.strip().split()

        for service_name in service_names:
            # Get the labels associated with the service to identify its pods
            get_service_labels_command = f"kubectl get service {service_name} -n {ns} -o=jsonpath='{{.spec.selector}}'"
            response = handle.run_native_cmd(get_service_labels_command)
            if not response.stdout.strip():
                print(f"No labels found for service {service_name} in namespace {ns}. Skipping...")
                continue
            labels_dict = json.loads(response.stdout.replace("'", "\""))
            label_selector = ",".join([f"{k}={v}" for k, v in labels_dict.items()])

            # Get the images from the pods associated with this service
            get_images_command = f"kubectl get pods -n {ns} -l {label_selector} -o=jsonpath='{{.items[*].spec.containers[*].image}}'"
            response = handle.run_native_cmd(get_images_command)
            if response and not response.stderr:
                # Deduplicate images and replace 'docker.io' with 'docker_io'
                images = list(set(response.stdout.strip().split()))
                images = [image.replace('docker.io', 'docker_io') for image in images]
                service_key = f"{service_name} ({ns})"
                service_images[service_key] = images
            else:
                service_key = f"{service_name} ({ns})"
                service_images[service_key] = []

    return service_images
