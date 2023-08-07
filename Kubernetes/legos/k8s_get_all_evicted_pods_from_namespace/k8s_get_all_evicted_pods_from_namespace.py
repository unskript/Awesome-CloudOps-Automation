#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#
import pprint
import json
from typing import Optional, Tuple
from pydantic import BaseModel, Field

from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='k8s Namespace')


def k8s_get_all_evicted_pods_from_namespace_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def k8s_get_all_evicted_pods_from_namespace(handle, namespace: str = "") -> Tuple:
    """k8s_get_all_evicted_pods_from_namespace returns all evicted pods

        :type handle: object
        :param handle: Object returned from the Task validate method
        
        :type namespace: str
        :param namespace: k8s namespace.

        :rtype: Tuple of status result and list of evicted pods
    """
    if handle.client_side_validation is not True:
        print(f"K8S Connector is invalid: {handle}")
        return False, None

    # Define the kubectl command based on the namespace input
    kubectl_command = "kubectl get pods --all-namespaces -o json"
    if namespace:
        kubectl_command = "kubectl get pods -n " + namespace + " -o json"

    try:
        response = handle.run_native_cmd(kubectl_command)
    except Exception as e:
        print(f"Error occurred while executing command {kubectl_command}: {str(e)}")
        raise e

    if response is None:
        print(f"Error while executing command ({kubectl_command}) (empty response)")
        raise e

    if response.stderr:
        raise ApiException(f"Error occurred while executing command {kubectl_command} {response.stderr}")

    result = []
    try:
        pod_details = json.loads(response.stdout)
        for pod in pod_details.get('items', []):
            if pod['status']['phase'] == 'Failed' and any(cs.get('reason') == 'Evicted' for cs in pod['status']['conditions']):
                pod_dict = {
                    "pod_name": pod["metadata"]["name"],
                    "namespace": pod["metadata"]["namespace"]
                }
                result.append(pod_dict)
    except Exception as e:
        raise e

    if result:
        return (False, result)
    return (True, None)
