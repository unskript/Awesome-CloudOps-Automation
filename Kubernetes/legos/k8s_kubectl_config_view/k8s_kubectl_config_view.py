from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    k8s_cli_string: str = Field(
        title='Kubectl Command',
        description='kubectl Displays merged kubeconfig settings',
        default='kubectl config view -n {namespace}'
    )
    namespace: str = Field(
        title='Namespace',
        description='Namespace'
    )

def k8s_kubectl_config_view_printer(data: str):
    if data is None:
        print("Error while executing command")
        return

    print (data)

def k8s_kubectl_config_view(handle, k8s_cli_string: str, namespace: str) -> str:
    """k8s_kubectl_config_view executes the given kubectl command

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type k8s_cli_string: str
        :param k8s_cli_string: kubectl Displays merged kubeconfig settings.

        :type namespace: str
        :param namespace: Namespace.

        :rtype: String, Output of the command in python string format or
        Empty String in case of Error.
    """
    k8s_cli_string = k8s_cli_string.format(namespace=namespace)
    result = handle.run_native_cmd(k8s_cli_string)
    if result is None or hasattr(result, "stderr") is False or result.stderr is None:
        return None

    return result.stdout
