[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>Get all K8s pods in ImagePullBackOff State </h1>

## Description
This Lego get all evicted pods in CrashLoopBackOff State from given namespace. If namespace not given it will get all the pods from all namespaces.


## Lego Details

    k8s_get_pods_in_crashloopbackoff_state(handle, namespace: str = None)

        handle: Object of type unSkript K8S Connector
        namespace: k8s namespace.(Optional)

## Lego Input

This Lego take two inputs handle, and namespace (Optional).


## Lego Output
Here is a sample output.
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)