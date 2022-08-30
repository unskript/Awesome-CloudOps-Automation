[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Kubectl rollout deployment</h2>

<br>

## Description
This Lego takes the `kubectl` command to be executed and returns the output of the command. This lego can be treated like a wrapper around the `kubectl` command.


## Lego Details

    k8s_kubectl_rollout_deployment(handle: object, k8s_cli_string: str, deployment: str, namespace: str)

        handle: Object of type unSkript MongoDB Connector
        k8s_cli_string: Kubectl command, eg: "kubectl get pods -A", "kubectl get ns"
        deployment: Deployment Name
        Namespace: namespace

## Lego Input
This Lego takes the actual k8s_cli_string, deployment and namespace to be executed as input, as python string.

Like all unSkript Legos this lego relies on the information provided in unSkript K8S Connector. 

>Note: The input for the command should start with keyword `kubectl` 


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://unskript.com)