[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>MongoDB Atlas cluster cloud backup</h1>

## Description
This Lego Trigger on-demand Atlas cloud backup.


## Lego Details

    mongodb_atlas_cluster_backup( handle, project_name: str, cluster_name: str, description: str, retention_in_days: int = 1)

        handle: Object of type unSkript Mongodb Connector.
        project_name : Atlas Project Name.
        project_name : Atlas Cluster Name.
        description : Description of the on-demand snapshot.
        retention_in_days: Number of days that Atlas should retain the on-demand snapshot. Must be at least 1.

## Lego Input
This Lego take five inputs handle, project_name, project_name,description and retention_in_days. 

## Lego Output
Here is a sample output.
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)