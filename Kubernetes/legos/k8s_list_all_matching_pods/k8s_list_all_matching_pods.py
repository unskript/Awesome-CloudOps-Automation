##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import pprint
import re
from typing import Optional, Tuple

from kubernetes import client
from pydantic import BaseModel, Field
from tabulate import tabulate

pp = pprint.PrettyPrinter(indent=2)


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='all',
        title='Namespace',
        description='Kubernetes namespace')
    matchstr: str = Field(
        title='Match String',
        description='''
                Matching name string. The matching string can be a regular expression too.
                For eg. ^[a-zA-Z0-9]+$ //string consists only of alphanumerics.
            ''')

def k8s_list_all_matching_pods_printer(output):
    if output is None:
        return
    
    (match_pods, data) = output
    if len(match_pods) > 0:
        print("\n")
        print(tabulate(data, tablefmt="grid", headers=[
            "Pod Ip", "Namespace", "Name", "Status", "Start Time"]))
    if not data:
        pp.pprint("No Matching Pods !!!")
    


def k8s_list_all_matching_pods(handle, matchstr: str, namespace: str = 'all') -> Tuple:
    """k8s_list_all_matching_pods list all matching pods

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type matchstr: str
        :param matchstr: Matching name string. The matching string can be a regular expression too.

        :type namespace: str
        :param namespace: Kubernetes namespace.

        :rtype: Tuple
    """
    coreApiClient = client.CoreV1Api(api_client=handle)

    data = []
    match_pods = []
    res = coreApiClient.list_namespaced_pod(namespace=namespace, pretty=True)
    if len(res.items) > 0:
        match_pods = list(filter(lambda x: (
            re.search(r'(%s)' % matchstr, x.metadata.name) != None), res.items))
        for pod in match_pods:
            data.append([pod.status.pod_ip, pod.metadata.namespace,
                         pod.metadata.name, pod.status.phase, pod.status.start_time])

    return (match_pods, data)
