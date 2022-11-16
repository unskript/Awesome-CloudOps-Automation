[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Kubectl in python syntax</h2>

<br>

## Description
This Lego takes the `kubectl` command to be executed and returns the output of the command. This lego can be treated like a wrapper around the `kubectl` command.


## Lego Details

    k8s_kubectl_command(handle: object, kubectl_command: str)

        handle: Object of type unSkript MongoDB Connector
        kubectl_command: Kubectl command, eg: "kubectl get pods -A", "kubectl get ns"

## Lego Input
This Lego takes the actual kubectl command to be executed as input, as python string.

Like all unSkript Legos this lego relies on the information provided in unSkript K8S Connector. 

>Note: The input for the command should start with keyword `kubectl` 

## Lego Output
Here is a sample output. For the command `kubectl describe pod {unhealthyPod} -n {namespace} | grep -A 10`

    Events:
    Type     Reason   Age                     From     Message
    ----     ------   ----                    ----     -------
    Normal   BackOff  33m (x437 over 133m)    kubelet  Back-off pulling image "diebian"
    Warning  Failed   3m16s (x569 over 133m)  kubelet  Error: ImagePullBackOff


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)