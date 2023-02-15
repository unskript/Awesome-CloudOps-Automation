#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

from pydantic import BaseModel, Field
from typing import Optional, Tuple
from collections import defaultdict
import json
import pprint
import re

class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='k8s Namespace')

def k8s_get_pods_in_imagepullbackoff_state_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def k8s_get_pods_in_imagepullbackoff_state(handle, namespace: str=None) -> Tuple:
    """k8s_get_list_of_pods_with_imagepullbackoff_state executes the given kubectl command to find pods in ImagePullBackOff State

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: Optional[str]
        :param namespace: Namespace to get the pods from. Eg:"logging", if not given all namespaces are considered

        :rtype: Status, List of pods in CrashLoopBackOff State and error if any 
    """
    if handle.client_side_validation != True:
        print(f"K8S Connector is invalid: {handle}")
        return str()
    kubectl_command ="kubectl get pods --all-namespaces | grep ImagePullBackOff | tr -s ' ' | cut -d ' ' -f 1,2"
    if namespace:
        kubectl_command = "kubectl get pods -n " + namespace + " | grep ImagePullBackOff | cut -d' ' -f 1 | tr -d ' '"
    response = handle.run_native_cmd(kubectl_command)
    if response is None or hasattr(response, "stderr") is False or response.stderr is None:
        print(
            f"Error while executing command ({kubectl_command}): {response.stderr}")
        return str()
    temp = response.stdout
    result = []
    res = []
    unhealthy_pods =[]
    unhealthy_pods_tuple = ()
    if not namespace:
        all_namespaces = re.findall(r"(\S+).*",temp)
        all_unhealthy_pods = re.findall(r"\S+\s+(.*)",temp)
        unhealthy_pods = [(i, j) for i, j in zip(all_namespaces, all_unhealthy_pods)]
        res = defaultdict(list)
        for key, val in unhealthy_pods:
            res[key].append(val)
    elif namespace:
        all_pods = []
        all_unhealthy_pods =[]
        all_pods = re.findall(r"(\S+).*",temp)
        for p in all_pods:
                unhealthy_pods_tuple = (namespace,p)
                unhealthy_pods.append(unhealthy_pods_tuple)
        res = defaultdict(list)
        for key, val in unhealthy_pods:
            res[key].append(val)
    result = dict(res)
    if len(result) != 0:
        return (False, result)
    else:
        return (True, [])
