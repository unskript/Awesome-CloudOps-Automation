#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from tabulate import tabulate

from kubernetes import client
from kubernetes.client.rest import ApiException



class InputSchema(BaseModel):
    namespace:Optional[str] = Field(
        default = "",
        title = "K8S Namespace",
        description = "Kubernetes Namespace Where the Service exists"
    )
    service_with_no_endpoint_whitelist: Optional[list] = Field(
        default = None,
        title = "Names of whitelisted services",
        description = "List of services for which this check should be skipped."
    )

def k8s_get_service_with_no_associated_endpoints_printer(output):
    status, data = output
    if status:
        print("No services with missing endpoints found !")
    else:
        table_headers = ["Namespace", "Service Name"]
        table_data = [(entry["namespace"], entry["name"]) for entry in data]

        print(tabulate(table_data, headers=table_headers, tablefmt = "grid"))

def k8s_get_service_with_no_associated_endpoints(handle, namespace: str = "", service_with_no_endpoint_whitelist = None) -> Tuple:
    """k8s_get_service_with_no_associated_endpoints This function returns Services that
       do not have any associated endpoints.

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :type namespace: str
       :param namespace: String, K8S Namespace as python string

       :rtype: Tuple Result in tuple format.
    """
    if handle.client_side_validation is not True:
        raise ApiException(f"K8S Connector is invalid {handle}")

    v1 = client.CoreV1Api(api_client=handle)

    # List services based on namespace
    if namespace:
        services = v1.list_namespaced_service(namespace=namespace).items
    else:
        services = v1.list_service_for_all_namespaces().items

    retval = []

    for service in services:
        if service_with_no_endpoint_whitelist is not None:
            if service.metadata.name in service_with_no_endpoint_whitelist:
                continue
        try:
            ep = v1.read_namespaced_endpoints(service.metadata.name, service.metadata.namespace)
            if not ep.subsets:
                retval.append({"name": service.metadata.name, "namespace": service.metadata.namespace})
        except ApiException as e:
            raise e

    if retval:
        return (False, retval)

    return(True, None)
