[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Get k8s cluster health</h2>

<br>

## Description
This Action returns the health of K8S cluster. This Action checks the following in a cluster
1. Abnormal Events that were reported
2. Node Resource Utilization 
3. Pod Resource Utilization
4. API Server readiness, liveness and health

If all these checks a boolean True value is returned, if not False and the reason for the failure is returned


## Lego Details

    k8s_get_cluster_health(handle: object)

        handle: Object of type unSkript K8S Connector

## Lego Input
This Lego takes handle (K8S) object returned from the task.validator(...)

## Lego Output
Here is a sample output.


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)