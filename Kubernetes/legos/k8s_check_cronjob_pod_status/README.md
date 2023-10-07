[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">]
(https://unskript.com/assets/favicon.png)
<h1>Checks the status of CronJob pods</h1>

## Description
This action checks the status of CronJob pods

## Lego Details
	k8s_check_cronjob_pod_status(handle, namespace: str="")
		handle: Object of type unSkript K8S Connector.
		cronjob_name: Name of the CronJob.
		schedule_interval: Optional, Expected running interval of the CronJob in minutes.


## Lego Input
This Lego takes inputs handle, cronjob_name, schedule_interval (Optional)

## Lego Output
Here is a sample output.
<img src="./1.png">
<img src="./2.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)