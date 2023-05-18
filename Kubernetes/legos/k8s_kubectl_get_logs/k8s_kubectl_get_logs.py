from pprint import pprint
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    k8s_cli_string: str = Field(
        title='Kubectl Command',
        description='kubectl get logs for a given pod',
        default='"kubectl logs {pod_name} -n {namespace}"'
    )
    pod_name: str = Field(
        title='Pod Name',
        description='Pod Name'
    )
    namespace: str = Field(
        title='Namespace',
        description='Namespace'
    )

def k8s_kubectl_get_logs_printer(data: str):
    if data is None:
        return

    print("Logs:")

    pprint(data)

def k8s_kubectl_get_logs(handle, k8s_cli_string: str, pod_name: str, namespace:str) -> str:
    """k8s_kubectl_get_logs executes the given kubectl command

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type k8s_cli_string: str
        :param k8s_cli_string: kubectl logs {pod_name} -n {namespace}.

        :type pod_name: str
        :param pod_name: Pod Name.

        :type namespace: str
        :param namespace: Namespace.

        :rtype: String, Output of the command in python string format or
        Empty String in case of Error.
    """
    k8s_cli_string = k8s_cli_string.format(pod_name=pod_name, namespace=namespace)
    result = handle.run_native_cmd(k8s_cli_string)
    data = result.stdout
    return data
