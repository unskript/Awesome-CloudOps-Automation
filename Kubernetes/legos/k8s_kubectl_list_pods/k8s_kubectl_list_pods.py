import io
import pandas as pd
from pydantic import BaseModel, Field
from kubernetes.client.rest import ApiException

class InputSchema(BaseModel):
    k8s_cli_string: str = Field(
        title='Kubectl Command',
        description='kubectl List pods in given namespace',
        default='kubectl get pods -n {namespace}'
    )
    namespace: str = Field(
        title='Namespace',
        description='Namespace'
    )

def k8s_kubectl_list_pods_printer(data: list):
    if data is None:
        return

    print("POD List:")

    for pod in data:
        print(f"\t {pod}")

def k8s_kubectl_list_pods(handle, k8s_cli_string: str, namespace: str) -> list:
    """k8s_kubectl_list_pods executes the given kubectl command

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type k8s_cli_string: str
        :param k8s_cli_string: kubectl get pods -n {namespace}.

        :type namespace: str
        :param namespace: Namespace.

        :rtype: 
    """
    k8s_cli_string = k8s_cli_string.format(namespace=namespace)
    result = handle.run_native_cmd(k8s_cli_string)
    if result is None:
        print(
            f"Error while executing command ({k8s_cli_string}) (empty response)")
        return []

    if result.stderr:
        raise ApiException(
            f"Error occurred while executing command {k8s_cli_string} {result.stderr}")

    df = pd.read_fwf(io.StringIO(result.stdout))
    all_pods = []
    for index, row in df.iterrows():
        all_pods.append(row['NAME'])
    return all_pods
