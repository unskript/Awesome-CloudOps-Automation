#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import pprint 

from typing import Tuple
from kubernetes import client
from kubernetes.client.rest import ApiException
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    namespace: str = Field(
        default = "",
        title = "K8S Namespace",
        description = "Kubernetes Namespace Where the Service exists"
    )

def k8s_get_service_with_no_associated_endpoints_printer(output):
    if output is None:
        return 
    
    print(output)

def k8s_get_service_with_no_associated_endpoints(handle, namespace: str = "") -> Tuple:
    """k8s_get_service_with_no_associated_endpoints This function returns Services that
       do not have any associated endpoints.

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :type namespace: str
       :param namespace: String, K8S Namespace as python string 

       :rtype: Tuple Result in tuple format.
    """
    if handle.client_side_validation != True:
        raise Exception(f"K8S Connector is invalid {handle}")
    
    v1 = client.CoreV1Api(api_client=handle)
    services = v1.list_service_for_all_namespaces().items
    services_to_check = services
    if namespace != "":
        for s in services:
            if s.metadata.namespace == namespace:
                services_to_check = s
                break
        
    retval = []
    for service in services_to_check:
        ep = v1.read_namespaced_endpoints(service.metadata.name, service.metadata.namespace)
        if not ep.subsets:
            pprint.pprint(ep)
            retval.append({"name": service.metadata.name, "namespace": service.metadata.namespace})

    if retval:
        return (False, retval)

    return(True, [])