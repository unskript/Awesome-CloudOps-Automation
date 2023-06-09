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

    kubectl_command = "kubectl get pods --all-namespaces -o json | grep Evicted"
    if namespace:
        kubectl_command = "kubectl get pods -n " + namespace + " -o json | grep Evicted"

    response = handle.run_native_cmd(kubectl_command)

    if response is None:
        print(
            f"Error while executing command ({kubectl_command}) (empty response)")
        return False, None
        
    if response.stderr:
        raise ApiException(f"Error occurred while executing command {kubectl_command} {response.stderr}")

    result = []
    try:
        pod_details = json.loads(response.stdout)
        for k, v in pod_details.items():
            if "items" in k:
                for i in v:
                    pod_dict = {}
                    pod_dict["pod_name"] = i["metadata"]["name"]
                    pod_dict["namespace"] = i["metadata"]["namespace"]
                    result.append(pod_dict)
    except Exception:
        pass

    if len(result) != 0:
        return (False, result)
    return (True, None)
