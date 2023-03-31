#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Tuple
from kubernetes import client
from kubernetes.client.rest import ApiException
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    pass

def k8s_get_service_with_no_associated_endpoints_printer(output):
    if output is None:
        return 
    
    print(output)

def k8s_get_service_with_no_associated_endpoints(handle) -> Tuple:
    """k8s_get_service_with_no_associated_endpoints This function returns Services that
       do not have any associated endpoints.

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :rtype: Tuple Result in tuple format.
    """
    if handle.client_side_validation != True:
        raise Exception(f"K8S Connector is invalid {handle}")
    
    v1 = client.CoreV1Api(api_client=handle)
    services = v1.list_service_for_all_namespaces().items
    retval = []
    for service in services:
        endpoints = v1.list_namespaced_endpoints(namespace=service.metadata.namespace, field_selector=f"metadata.name={service.metadata.name}").items
        if not endpoints:
            retval.append(service)

    if retval:
        return (False, retval)

    return(True, [])