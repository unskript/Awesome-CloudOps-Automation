from pprint import pprint
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    pod_name: str = Field(
        title='Pod Name',
        description='Pod Name'
    )
    k8s_cli_string: str = Field(
        title='Kubectl Command',
        description='kubectl describe a pod',
        default='kubectl describe pod {pod_name} -n {namespace}'
    )
    namespace: str = Field(
        title='Namespace',
        description='Namespace'
    )

def k8s_kubectl_describe_pod_printer(data: str):
    if data is None:
        return
    print("Pod Details:")
    pprint(data)

def k8s_kubectl_describe_pod(handle, pod_name: str, k8s_cli_string: str, namespace: str) -> str:
    """k8s_kubectl_describe_pod executes the given kubectl command

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type k8s_cli_string: str
        :param k8s_cli_string: kubectl describe pod {pod_name} -n {namespace}.

        :type node_name: str
        :param node_name: Node Name.

        :type namespace: str
        :param namespace:Namespace

        :rtype: String, Output of the command in python string format or
        Empty String in case of Error.
    """
    k8s_cli_string = k8s_cli_string.format(pod_name=pod_name, namespace=namespace)
    result = handle.run_native_cmd(k8s_cli_string)
    data = result.stdout
    return data
