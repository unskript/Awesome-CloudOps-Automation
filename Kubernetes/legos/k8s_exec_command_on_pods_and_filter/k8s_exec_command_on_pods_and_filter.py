#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
import pprint
import re
from typing import List, Dict
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.stream import stream


class InputSchema(BaseModel):
    namespace: str = Field(
        title='Namespace',
        description='Kubernetes namespace.')
    pods: list = Field(
        title='Pod(s)',
        description='Kubernetes Pod Name(s)')
    match: str = Field(
        title='Match String',
        description='Matching String for Command response'
    )
    command: list = Field(
        title='Command',
        description='List of Commands to Execute on the Pod, '
        'ex: ["/bin/sh","-c","nslookup google.com"]')

def legoPrinter(output):
    if output is None:
        return

    pprint.pprint(output)


def k8s_exec_command_on_pods_and_filter(
        handle,
        namespace: str,
        pods: List,
        match: str,
        command: List
        ) -> Dict:

    """k8s_exec_command_on_pods_and_filter executes the given kubectl command on the pod

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Kubernetes namespace.

        :type pods: List
        :param pods: Kubernetes Pod Name(s).

        :type match: str
        :param match: Matching String for Command response.

        :type command: List
        :param command: List of Commands to Execute on the Pod.

        :rtype: String, Output of the command in python string 
        format or Empty String in case of Error.
    """
    coreApiClient = client.CoreV1Api(api_client=handle)

    result = {}
    try:
        for pod in pods:
            resp = stream(coreApiClient.connect_get_namespaced_pod_exec,
                          pod,
                          namespace,
                          command=list(command),
                          stderr=True,
                          stdin=True,
                          stdout=True,
                          tty=False
                          )
            res = re.search(f'({match})', resp)
            if res is not None:
                result['name'] = pod
                result['output'] = res
                result['status'] = 'SUCCESS'
    except Exception as e:
        result['name'] = 'N/A'
        result['output'] = e
        result['status'] = 'ERROR'

    return result
