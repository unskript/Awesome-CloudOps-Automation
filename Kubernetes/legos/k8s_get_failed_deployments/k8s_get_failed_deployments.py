#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import List
from pydantic import BaseModel, Field
from kubernetes.client.rest import ApiException
import json


class InputSchema(BaseModel):
    namespace: str = Field(
        '',
        description="K8S Namespace",
        title="K8S Namespace"
    )

def k8s_get_failed_deployments_printer(output):
    if output is None:
        return
    print(output)


def k8s_get_failed_deployments(handle, namespace: str = '') -> List:
    """k8s_get_failed_deployments Returns all failed deployments across all namespaces
    or within a specific namespace if provided. The deployments are considered
    failed if the 'Available' condition is set to 'False'.

    :type handle: Object
    :param handle: Object returned from task.validate(...) function

    :type namespace: str
    :param namespace: The specific namespace to filter the deployments. Defaults to ''.

    :rtype: Status of result, list of dictionaries, each containing the 'name' and 'namespace' of the failed deployments.
    """
    # Construct the kubectl command based on whether a namespace is provided
    kubectl_command = "kubectl get deployments --all-namespaces -o json"
    if namespace:
        kubectl_command = "kubectl get deployments -n " + namespace + " -o json"
    # Execute kubectl command
    response = handle.run_native_cmd(kubectl_command)
    # Check if the response is None, which indicates an error
    if response is None:
        print(f"Error while executing command ({kubectl_command}) (empty response)")
    if response.stderr:
        raise ApiException(f"Error occurred while executing command {kubectl_command} {response.stderr}")

    result = []
    try:
        deployments = json.loads(response.stdout)
        # Iterate over each item in the deployments
        for item in deployments["items"]:
            # Check each condition of the deployment
            for condition in item["status"]["conditions"]:
                # If the 'Available' condition is set to 'False', add the deployment to the result
                if condition["type"] == "Available" and condition["status"] == "False":
                    result.append({
                        'name': item["metadata"]["name"],
                        'namespace': item["metadata"]["namespace"]
                    })
    except Exception as e:
        raise e

    return (False, result) if result else (True, None)