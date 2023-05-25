from pydantic import BaseModel, Field
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    k8s_cli_string: str = Field(
        title='Kubectl Command',
        description='kubectl Show metrics for a given node',
        default='kubectl top node {node_name}'
    )
    node_name: str = Field(
        title='Node Name',
        description='Node Name'
    )


def k8s_kubectl_show_metrics_node_printer(data: str):
    if data is None:
        print("Error while executing command")
        return

    print(data)


def k8s_kubectl_show_metrics_node(handle, k8s_cli_string: str, node_name: str) -> str:
    """k8s_kubectl_show_metrics_node executes the given kubectl command

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type k8s_cli_string: str
        :param k8s_cli_string: kubectl top node {node_name}.

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
        raise ApiException(
            f"Error occurred while executing command {k8s_cli_string} {result.stderr}")

    return result.stdout
