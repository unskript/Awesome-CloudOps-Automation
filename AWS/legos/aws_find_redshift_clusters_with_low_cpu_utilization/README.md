[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">]
(https://unskript.com/assets/favicon.png)
<h1>AWS Find Redshift Clusters with low CPU Utilization</h1>

## Description
Find underutilized Redshift clusters in terms of CPU utilization.

## Lego Details
	aws_find_redshift_clusters_with_low_cpu_utilization(handle, utilization_threshold:int=10, region: str = "", duration_minutes:int=5)
		handle: Object of type unSkript AWS Connector.
		utilization_threshold: The threshold percentage of CPU utilization for a Redshift Cluster.
		duration_minutes: The threshold percentage of CPU utilization for a Redshift Cluster.

## Lego Input
This Lego takes inputs handle, utilization_threshold, duration_minutes

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)