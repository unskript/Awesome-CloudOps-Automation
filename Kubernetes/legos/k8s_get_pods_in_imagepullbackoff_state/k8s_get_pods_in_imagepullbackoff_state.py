#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

import pprint
import re
from typing import Optional, Tuple
from collections import defaultdict
from pydantic import BaseModel, Field

from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='k8s Namespace')


def k8s_get_pods_in_imagepullbackoff_state_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def k8s_get_pods_in_imagepullbackoff_state(handle, namespace: str = '') -> Tuple:
    """k8s_get_list_of_pods_with_imagepullbackoff_state executes the given
    kubectl command to find pods in ImagePullBackOff State

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: Optional[str]
        :param namespace: Namespace to get the pods from. Eg:"logging",
        if not given all namespaces are considered

        :rtype: Status, List of pods in CrashLoopBackOff State
    """
    if handle.client_side_validation is not True:
        print(f"K8S Connector is invalid: {handle}")
        return False, None

    kubectl_command = ("kubectl get pods --all-namespaces | grep -e ImagePullBackOff -e ErrImagePull "
                       "| tr -s ' ' | cut -d ' ' -f 1,2")
    if namespace:
        kubectl_command = "kubectl get pods -n " + namespace + \
            " | grep -e ImagePullBackOff -e ErrImagePull | cut -d' ' -f 1 | tr -d ' '"
    response = handle.run_native_cmd(kubectl_command)

    if response is None:
        print(
            f"Error while executing command ({kubectl_command}) (empty response)")
        return False, None

    if response.stderr:
        raise ApiException(
            f"Error occurred while executing command {kubectl_command} {response.stderr}")

    temp = response.stdout
    result = []
    res = []
    unhealthy_pods = []
    unhealthy_pods_tuple = ()
    if not namespace:
        all_namespaces = re.findall(r"(\S+).*", temp)
        all_unhealthy_pods = re.findall(r"\S+\s+(.*)", temp)
        unhealthy_pods = list(zip(all_namespaces, all_unhealthy_pods))
        res = defaultdict(list)
        for key, val in unhealthy_pods:
            res[key].append(val)
    elif namespace:
        all_pods = []
        all_unhealthy_pods = []
        all_pods = re.findall(r"(\S+).*", temp)
        for p in all_pods:
            unhealthy_pods_tuple = (namespace, p)
            unhealthy_pods.append(unhealthy_pods_tuple)
        res = defaultdict(list)
        for key, val in unhealthy_pods:
            res[key].append(val)
    if len(res) != 0:
        result.append(dict(res))
    if len(result) != 0:
        return (False, result)
    return (True, None)
