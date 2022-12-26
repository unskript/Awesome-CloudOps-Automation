#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

from pydantic import BaseModel, Field
from typing import Optional, List
import pprint
import json

class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='k8s Namespace')


def k8s_get_all_evicted_pods_from_namespace_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def k8s_get_all_evicted_pods_from_namespace(handle, namespace: str = "") -> List:
    """k8s_kubectl_command executes the given kubectl command on the pod

        :type handle: object
        :param handle: Object returned from the Task validate method
        
        :type namespace: str
        :param namespace: k8s namespace.

        :rtype: Tuple
    """
    if handle.client_side_validation != True:
        print(f"K8S Connector is invalid: {handle}")
        return str()

    kubectl_command = "kubectl get pods --all-namespaces -o json | grep Evicted"
    if namespace:
        kubectl_command = "kubectl get pods -n " + namespace + " -o json | grep Evicted"

    response = handle.run_native_cmd(kubectl_command)
    if response is None or hasattr(response, "stderr") is False or response.stderr is None:
        print(
            f"Error while executing command ({kubectl_command}): {response.stderr}")
        return str()

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
    except Exception as e:
        pass
    
    execution_flag = False
    if len(result) > 0:
        execution_flag = True
    output = (execution_flag, result)
    return output
    
