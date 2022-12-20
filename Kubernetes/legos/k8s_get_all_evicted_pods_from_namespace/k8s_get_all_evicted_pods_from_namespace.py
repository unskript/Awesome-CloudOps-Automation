#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

from pydantic import BaseModel, Field
from typing import Optional, List
import pprint
import pandas as pd
import io

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

    kubectl_command = "kubectl get pods --all-namespaces | grep Evicted"
    if namespace:
        kubectl_command = "kubectl get pods -n " + namespace + " | grep Evicted"

    result = handle.run_native_cmd(kubectl_command)
    if result is None or hasattr(result, "stderr") is False or result.stderr is None:
        print(
            f"Error while executing command ({kubectl_command}): {result.stderr}")
        return str()

    all_pods = []
    try:
        df = pd.read_fwf(io.StringIO(result.stdout))
        for index, row in df.iterrows():
            all_pods.append(row['NAME'])
        return all_pods
    except Exception as e:
        return all_pods
