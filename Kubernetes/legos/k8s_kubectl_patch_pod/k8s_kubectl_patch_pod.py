from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    k8s_cli_string: str = Field(
        title='Kubectl Command',
        description='kubectl update field of a resource using strategic merge patch',
        default="kubectl patch pod {pod_name} -p '{patch}' -n {namespace}"
    )
    pod_name: str = Field(
        title='Pod Name',
        description='Pod Name'
    )
    patch: str = Field(
        title='Patch',
        description='The patch to be applied to the resource'
    )
    namespace: str = Field(
        title='Namespace',
        description='Namespace'
    )

def k8s_kubectl_patch_pod_printer(data: str):
    if data is None:
        print("Error while executing command")
        return

    print (data)

def k8s_kubectl_patch_pod(
        handle,
        k8s_cli_string: str,
        pod_name:str,
        patch: str,
        namespace: str
        ) -> str:
    """k8s_kubectl_patch_pod executes the given kubectl command

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type k8s_cli_string: str
        :param k8s_cli_string: kubectl patch pod {pod_name} -p '{patch}' -n {namespace}.

        :type pod_name: str
        :param pod_name: Pod Name.

        :type patch: str
        :param patch: The patch to be applied to the resource.

        :type namespace: str
        :param namespace: Namespace.

        :rtype: String, Output of the command in python string format or
        Empty String in case of Error.
    """
    k8s_cli_string = k8s_cli_string.format(pod_name=pod_name, patch=patch, namespace=namespace)
    result = handle.run_native_cmd(k8s_cli_string)
    if result is None or hasattr(result, "stderr") is False or result.stderr is None:
        return None

    return result.stdout
