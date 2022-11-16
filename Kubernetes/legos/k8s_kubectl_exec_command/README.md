[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Kubectl execute command</h2>

<br>

## Description
This Lego Kubectl execute command in a given pod.


## Lego Details

    k8s_kubectl_exec_command(handle: object, k8s_cli_string: str, pod_name:str, command: str, namespace: str)

        handle: Object of type unSkript K8S Connector
        k8s_cli_string: kubectl exec {pod_name} {command} -n {namespace}.
        pod_name: Pod Name.
        command: Command.
        namespace: Namespace.

## Lego Input
This Lego take five input handle, k8s_cli_string, pod_name, command and namespace.

## Lego Output
Here is a sample output.
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)