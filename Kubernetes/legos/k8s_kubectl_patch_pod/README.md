[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Kubectl update field</h2>

<br>

## Description
This Lego Kubectl update field of a resource using strategic merge patch.


## Lego Details

    k8s_kubectl_patch_pod(handle: object, k8s_cli_string: str, pod_name:str, patch: str, namespace: str)

        handle: Object of type unSkript K8S Connector
        k8s_cli_string: kubectl drain {node_name}.
        pod_name: Pod Name.
        patch: The patch to be applied to the resource.
        namespace: Namespace.

## Lego Input
This Lego take five input handle, k8s_cli_string, pod_name, patch and namespace.

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)