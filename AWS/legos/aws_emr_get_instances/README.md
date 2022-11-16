[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>Get AWS EMR Instances </h1>

## Description
This Lego get a list of EC2 Instances for an EMR cluster. Filtered by node type (MASTER|CORE|TASK)


## Lego Details

    aws_emr_get_instances(handle: object, cluster_id: str, instance_group_type: str, region: str)

        handle: Object of type unSkript AWS Connector.
        cluster_id: Cluster ID for the EMR cluster.
        instance_group_type: Group type to filter on.
        region: AWS Region of the cluster

## Lego Input

This Lego take four inputs handle, cluster_id, instance_group_type and region.


## Lego Output
Here is a sample output.
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)