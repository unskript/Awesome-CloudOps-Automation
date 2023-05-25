from pprint import pprint
from pydantic import BaseModel, Field
from kubernetes.client.rest import ApiException

class InputSchema(BaseModel):
    k8s_cli_string: str = Field(
        title='Kubectl Command',
        description='kubectl get api resources',
        default='kubectl api-resources -o wide -n {namespace}'
    )
    namespace: str = Field(
        title='Namespace',
        description='Namespace',
    )

def k8s_kubectl_get_api_resources_printer(data: str):
    if data is None:
        print("Error while executing command")
        return

    pprint (data)

def k8s_kubectl_get_api_resources(handle, k8s_cli_string: str, namespace: str) -> str:
    """k8s_kubectl_get_api_resources executes the given kubectl command

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type k8s_cli_string: str
        :param k8s_cli_string: kubectl api-resources -o wide -n {namespace}.

        :type namespace: str
        :param namespace: Namespace.

        :rtype: String, Output of the command in python string format or
        Empty String in case of Error.
    """
    k8s_cli_string = k8s_cli_string.format(namespace=namespace)
    result = handle.run_native_cmd(k8s_cli_string)

    if result is None:
        print(
            f"Error while executing command ({k8s_cli_string}) (empty response)")
        return False, None
        
    if result.stderr:
        raise ApiException(f"Error occurred while executing command {k8s_cli_string} {result.stderr}")

    return result.stdout
