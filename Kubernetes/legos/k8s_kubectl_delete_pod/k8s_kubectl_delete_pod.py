from pydantic import BaseModel, Field
from kubernetes.client.rest import ApiException

class InputSchema(BaseModel):
    k8s_cli_string: str = Field(
        title='Kubectl Command',
        description='kubectl delete a pod',
        default='kubectl delete pod {pod_name} -n {namespace}'
    )
    pod_name: str = Field(
        title='Pod Name',
        description='Pod Name'
    )
    namespace: str = Field(
        title='Namespace',
        description='Namespace'
    )

def k8s_kubectl_delete_pod_printer(data: str):
    if data is None:
        print("Error while executing command")
        return

    print (data)

def k8s_kubectl_delete_pod(handle, k8s_cli_string: str, pod_name: str, namespace: str) -> str:
    """k8s_kubectl_delete_pod executes the given kubectl command

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type k8s_cli_string: str
        :param k8s_cli_string: kubectl delete pod {pod_name} -n {namespace}.

        :type pod_name: str
        :param pod_name: Pod Name.

        :type namespace: str
        :param namespace: Namespace.

        :rtype: String, Output of the command in python string format or
        Empty String in case of Error.
    """
    k8s_cli_string = k8s_cli_string.format(pod_name, namespace)
    result = handle.run_native_cmd(k8s_cli_string)

    if result is None:
        print(
            f"Error while executing command ({k8s_cli_string}) (empty response)")
        return ""
        
    if result.stderr:
        raise ApiException(f"Error occurred while executing command {k8s_cli_string} {result.stderr}")
    return result.stdout
