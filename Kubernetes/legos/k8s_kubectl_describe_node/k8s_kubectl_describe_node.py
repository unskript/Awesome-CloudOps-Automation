from pprint import pprint
from pydantic import BaseModel, Field
from kubernetes.client.rest import ApiException

class InputSchema(BaseModel):
    node_name: str = Field(
        title='Node Name',
        description='Node Name'
    )
    k8s_cli_string: str = Field(
        title='Kubectl Command',
        description='kubectl describe a node',
        default='kubectl describe node {node_name}'
    )

def k8s_kubectl_describe_node_printer(data: str):
    if data is None:
        return

    print("Node Details:")
    pprint(data)

def k8s_kubectl_describe_node(handle, node_name: str, k8s_cli_string: str) -> str:
    """k8s_kubectl_describe_node executes the given kubectl command

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type k8s_cli_string: str
        :param k8s_cli_string: kubectl describe node {node_name}.

         :type node_name: str
        :param node_name: Node Name.

        :rtype: String, Output of the command in python string format or
        Empty String in case of Error.
    """

    k8s_cli_string = k8s_cli_string.format(node_name=node_name)
    result = handle.run_native_cmd(k8s_cli_string)
    if result is None:
        print(
            f"Error while executing command ({k8s_cli_string}) (empty response)")
        return False, None
        
    if result.stderr:
        raise ApiException(f"Error occurred while executing command {k8s_cli_string} {result.stderr}")


    data = result.stdout
    return data
