[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Kubernetes Execute a command on a POD</h2>

<br>

## Description
This Lego execute a command on Kubernetes POD in a given namespace and filter output.


## Lego Details

    k8s_exec_command_on_pods_and_filter(handle: object, namespace: str, pods: List, match: str, command: List)

        handle: Object of type unSkript K8S Connector
        namespace: Kubernetes namespace.
        pods: Kubernetes Pod Name(s).
        match: Matching String for Command response.
        command: List of Commands to Execute on the Pod.

## Lego Input
This Lego take five input handle, namespace, pods, match and command.

## Lego Output
Here is a sample output.


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)