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

def k8s_get_failed_deployments_printer(output):
    if output is None:
        return 
    
    print(output)


def k8s_get_failed_deployments(handle) -> Tuple:
    """k8s_get_failed_deployments Returns the list of all failed deployments across all namespaces

    :type handle: Object
    :param handle: Object returned from task.validate(...) function

    :rtype: Tuple of the result
    """
    if handle.client_side_validation != True:
        raise Exception(f"K8S Connector is invalid {handle}")

    apps_client = client.AppsV1Api(api_client=handle)
    deployments = apps_client.list_deployment_for_all_namespaces().items 
    retval = {} 
    for deployment in deployments:
        # FIXME. Check for deployment.status.condition 
        if deployment.status.available_replicas == 0:
            retval.update(deployment)
    
    # FIXME: Add print for diagnostic. 
    # Return deployment name and namespace in a Tuple. 
    if not retval:
        return (False, [retval])
    
    return (True, [])