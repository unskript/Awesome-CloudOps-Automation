#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

from pydantic import BaseModel, Field
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    kubectl_command: str = Field(
        title='Kubectl Command',
        description='kubectl command '
                    'eg "kubectl get pods --all-namespaces"'
    )


def k8s_kubectl_command_printer(output):
    if output is None:
        return
    print(output)


def k8s_kubectl_command(handle, kubectl_command: str) -> str:
    """k8s_kubectl_command executes the given kubectl command on the pod

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type kubectl_command: str
        :param kubectl_command: The Actual kubectl command, like kubectl get ns, etc..

        :rtype: String, Output of the command in python string format or Empty String
        in case of Error.
    """
    if handle.client_side_validation is not True:
        print(f"K8S Connector is invalid: {handle}")
        return str()

    result = handle.run_native_cmd(kubectl_command)

    if result is None:
        print(
            f"Error while executing command ({kubectl_command}) (empty response)")
        return False, None
        
    if result.stderr:
        raise ApiException(f"Error occurred while executing command {kubectl_command} {result.stderr}")

    return result.stdout
