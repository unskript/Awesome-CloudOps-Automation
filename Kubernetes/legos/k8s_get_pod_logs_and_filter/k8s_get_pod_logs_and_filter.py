##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import re
import pprint
from typing import List, Dict
from pydantic import BaseModel, Field
from kubernetes import client


class InputSchema(BaseModel):
    namespace: str = Field(
        title='Namespace',
        description='k8s namespace')
    pods: list = Field(
        title='Pods',
        description='Name of pods')
    matchstr: str = Field(
        title='Match String',
        description='String to Match in the Logs')

def k8s_get_pod_logs_and_filter_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def k8s_get_pod_logs_and_filter(handle, namespace: str, pods: List, matchstr: str) -> Dict:
    """k8s_get_pod_logs_and_filter get pod logs

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: k8s namespace.

        :type pods: List
        :param pods: Name of pods.

        :type matchstr: str
        :param matchstr: String to Match in the Logs.

        :rtype: Dict
    """
    coreApiClient = client.CoreV1Api(api_client=handle)

    result = {}
    try:
        for pod in pods:
            resp = coreApiClient.read_namespaced_pod_log(
                namespace=namespace, name=pod, pretty=True, timestamps=True)
            res = re.search(f'({matchstr})', resp)
            if res is not None:
                result[pod] = res

    except Exception:
        print("Unable to Read Logs from the Pods")

    return result
