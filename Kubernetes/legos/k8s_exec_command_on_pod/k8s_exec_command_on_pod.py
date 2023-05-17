#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
import pprint
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.stream import stream


class InputSchema(BaseModel):
    namespace: str = Field(
        title='Namespace',
        description='Kubernetes namespace.')
    podname: str = Field(
        title='Pod',
        description='Kubernetes Pod Name')
    command: str = Field(
        title='Command',
        description='Commands to execute on the Pod. Eg "df -k"')

def k8s_exec_command_on_pod_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def k8s_exec_command_on_pod(handle, namespace: str, podname: str, command: str) -> str:
    """k8s_exec_command_on_pod executes the given kubectl command on the pod

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Kubernetes namespace.

        :type podname: str
        :param podname: Kubernetes Pod Name.

        :type command: str
        :param command: Commands to execute on the Pod.

        :rtype: String, Output of the command in python string format 
        or Empty String in case of Error.
    """
    coreApiClient = client.CoreV1Api(api_client=handle)

    try:
        resp = stream(coreApiClient.connect_get_namespaced_pod_exec,
                      podname,
                      namespace,
                      command=command.split(),
                      stderr=True,
                      stdin=True,
                      stdout=True,
                      tty=False
                      )
    except Exception as e:
        resp = f'An Exception occured while executing the command {e}'

    return resp
