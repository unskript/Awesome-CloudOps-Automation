[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Detect K8s services crashes</h2>

<br>

## Description
This action detects service crashes by checking the logs of each pod for specific error messages.


## Lego Details

    k8s_detect_service_crashes(handle, namespace: str, core_services: list, tail_lines: int = 100)

        handle: Object of type unSkript K8S Connector
        namespace: Kubernetes namespace
        core_services: List of services to detect service crashes
        tail_lines: Number of log lines to fetch from each container. Defaults to 100.

## Lego Input
This Lego take 4 inputs handle, namespace, tail_lines, core_services.

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)