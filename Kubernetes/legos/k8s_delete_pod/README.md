[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Delete a Kubernetes POD</h2>

<br>

## Description
This Lego delete a Kubernetes POD in a given Namespace.


## Lego Details

    k8s_delete_pod(handle: object, namespace: str, podname: str)

        handle: Object of type unSkript MongoDB Connector
        namespace: Kubernetes namespace
        podname: K8S Pod Name

## Lego Input
This Lego take three input handle, namespace and podname.

## Lego Output
Here is a sample output. For the command `kubectl describe pod {unhealthyPod} -n {namespace} | grep -A 10`

    Events:
    Type     Reason   Age                     From     Message
    ----     ------   ----                    ----     -------
    Normal   BackOff  33m (x437 over 133m)    kubelet  Back-off pulling image "diebian"
    Warning  Failed   3m16s (x569 over 133m)  kubelet  Error: ImagePullBackOff


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)