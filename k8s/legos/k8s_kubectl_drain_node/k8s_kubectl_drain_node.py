from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    k8s_cli_string: str = Field(
        title='Kubectl Command',
        description='kubectl drain a node in preparation of a maintenance',
        default='kubectl drain {node_name}'
    )
    node_name: str = Field(
        title='Node Name',
        description='Node Name'
    )

def k8s_kubectl_drain_node_printer(data: str):
    if data is None:
        print("Error while executing command")
        return

    print (data)

def k8s_kubectl_drain_node(handle, k8s_cli_string: str, node_name:str) -> str:
    """k8s_kubectl_drain_node executes the given kubectl command

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type k8s_cli_string: str
        :param k8s_cli_string: kubectl drain {node_name}.

        :type node_name: str
        :param node_name: Node Name.

        :rtype: String, Output of the command in python string format or Empty String in case of Error.
    """
    k8s_cli_string = k8s_cli_string.format(node_name=node_name)
    result = handle.run_native_cmd(k8s_cli_string)
    if result is None or hasattr(result, "stderr") is False or result.stderr is None:
        return None

    return result.stdout
