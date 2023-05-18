import io
import pandas as pd
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    k8s_cli_string: str = Field(
        title='Kubectl Command',
        description='kubectl list services in current namespace',
        default='kubectl get service -n {namespace}'
    )
    namespace: str = Field(
        title='Namespace',
        description='Namespace'
    )

def k8s_kubectl_get_service_namespace_printer(data: list):
    if data is None:
        return

    print("Service List:")

    for service in data:
        print(f"\t {service}")

def k8s_kubectl_get_service_namespace(handle, k8s_cli_string: str, namespace: str) -> list:
    """k8s_kubectl_get_service_namespace executes the given kubectl command

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type k8s_cli_string: str
        :param k8s_cli_string: kubectl get service -n {namespace}.

        :type namespace: str
        :param namespace: Namespace.

        :rtype: 
    """
    k8s_cli_string = k8s_cli_string.format(namespace=namespace)
    result = handle.run_native_cmd(k8s_cli_string)
    df = pd.read_fwf(io.StringIO(result.stdout))
    all_services = []
    for index, row in df.iterrows():
        all_services.append(row['NAME'])
    return all_services
