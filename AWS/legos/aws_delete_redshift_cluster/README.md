[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">]
(https://unskript.com/assets/favicon.png)
<h1>AWS Delete Redshift Cluster</h1>

## Description
Delete AWS Redshift Cluster

## Lego Details
	aws_delete_redshift_cluster(handle, region: str, cluster_identifier: str, skip_final_cluster_snapshot:bool=False)
		handle: Object of type unSkript AWS Connector.
		skip_final_cluster_snapshot: Determines whether a final snapshot of the cluster is created before Amazon Redshift deletes the cluster. If true, a final cluster snapshot is not created. If false, a final cluster snapshot is created before the cluster is deleted.
		cluster_identifier: The identifier of the cluster to be deleted.


## Lego Input
This Lego takes inputs handle, cluster_identifier, skip_final_cluster_snapshot.

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)