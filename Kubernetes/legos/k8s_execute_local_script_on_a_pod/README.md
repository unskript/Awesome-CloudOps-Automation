[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Execute Local Script on a Pod</h2>

<br>

## Description
Execute a given script on a pod in a namespace

## Lego Details

    k8s_execute_local_script_on_a_pod(handle: object, pod_name: str, namespace: str, script_text:str)

        handle: Object of type unSkript K8S Connector
        pod_name: String, Name of the POD (Mandatory parameter)
        namespace: String, Namespace where the POD exists
        script_text: String, Text data of the script that needs to be run on the pod.

## Lego Input
This Lego takes four mandatory inputs. Handle (K8S) object returned from the task.validator(...),
POD Name and Namespace where the POD exists, local script TEXT that needs to be run on the pod. 

## Lego Output
Here is a sample output-
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)