[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>Plot AWS PostgreSQL Active Connections</h1>

## Description
This Lego Plot AWS PostgreSQL Active Connections


## Lego Details

    aws_postgresql_plot_active_connections(handle: object, cluster_identifier: str, max_connections: int, time_since: int, region: str)
        handle: Object of type unSkript AWS Connector.
        cluster_identifier: RDS DB Identifier.
        max_connections: Configured max connections.
        time_since: Starting from now, window (in seconds) for which you want to get the datapoints for.
        region: AWS Region of the Postgres DB Cluster.
## Lego Input

This Lego take five inputs handle, cluster_identifier, max_connections, time_since and region.


## Lego Output
Here is a sample output.
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)