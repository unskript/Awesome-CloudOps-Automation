from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    k8s_cli_string: str = Field(
        title='Kubectl Command',
        description='kubectl Scale a given deployment',
        default='kubectl scale --replicas={num} deployment {deployment} -n {namespace}'
    )
    num: str = Field(
        title='Specified Size',
        description='Specified Size'
    )
    deployment: str = Field(
        title='Deployment Name',
        description='Deployment Name'
    )
    namespace: str = Field(
        title='Namespace',
        description='Namespace'
    )

def k8s_kubectl_scale_deployment_printer(data: str):
    if data is None:
        print("Error while executing command")
        return

    print (data)

def k8s_kubectl_scale_deployment(handle, k8s_cli_string: str, num: str, deployment: str, namespace:str) -> str:
    """k8s_kubectl_scale_deployment executes the given kubectl command

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type k8s_cli_string: str
        :param k8s_cli_string: kubectl scale --replicas={num} deployment {deployment} -n {namespace}.

        :type num: str
        :param num: Specified Size.

        :type deployment: str
        :param deployment: Deployment Name.

        :type namespace: str
        :param namespace: Namespace.

        :rtype: String, Output of the command in python string format or Empty String in case of Error.
    """
    k8s_cli_string = k8s_cli_string.format(num=num, deployment=deployment, namespace=namespace)
    result = handle.run_native_cmd(k8s_cli_string)
    if result is None or hasattr(result, "stderr") is False or result.stderr is None:
        return None

    return result.stdout
