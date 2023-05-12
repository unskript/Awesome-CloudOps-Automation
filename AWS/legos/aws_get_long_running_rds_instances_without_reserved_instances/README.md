[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">]
(https://unskript.com/assets/favicon.png)
<h1>AWS Get Long Running RDS Instances Without Reserved Instances</h1>

## Description
This action gets information about long running instances and their status, and checks if they have any reserved nodes associated with them.

## Lego Details
	aws_get_long_running_rds_instances_without_reserved_instances(handle, region: str = "", threshold:int=10)
		handle: Object of type unSkript AWS Connector.
		threshold: Threshold(in days) to find long running RDS instances. Eg: 30, This will find all the instances that have been created a month ago.


## Lego Input
This Lego takes inputs handle,threshold.

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)