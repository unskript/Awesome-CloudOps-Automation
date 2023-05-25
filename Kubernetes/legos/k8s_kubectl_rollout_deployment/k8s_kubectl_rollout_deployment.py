#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

from pydantic import BaseModel, Field
from beartype import beartype
from kubernetes.client.rest import ApiException

class InputSchema(BaseModel):
    k8s_cli_string: str = Field(
        title='Kubectl Command',
        description='kubectl command '
                    'eg "kubectl get pods --all-namespaces"'
    )
    deployment: str = Field(
        title='Deployment Name',
        description='Deployment Name'
    )
    namespace: str = Field(
        title='Namespace',
        description='Namespace'
    )


@beartype
def k8s_kubectl_rollout_deployment_printer(data: str):
    if data is None:
        print("Error while executing command")
        return

    print (data)

@beartype
def k8s_kubectl_rollout_deployment(
    handle,
    k8s_cli_string: str,
    deployment: str,
    namespace: str
    ) -> str:
    k8s_cli_string = k8s_cli_string.format(deployment=deployment, namespace=namespace)
    result = handle.run_native_cmd(k8s_cli_string)

    if result is None:
        print(
            f"Error while executing command ({k8s_cli_string}) (empty response)")
        return None

    if result.stderr:
        raise ApiException(
            f"Error occurred while executing command {k8s_cli_string} {result.stderr}")

    return result.stdout

## Duplicate code?