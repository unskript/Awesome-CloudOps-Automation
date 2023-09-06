[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">]
(https://unskript.com/assets/favicon.png)
<h1>PostgreSQL check active connections</h1>

## Description
Checks if the percentage of active connections to the database exceeds the provided threshold.

## Lego Details
	postgresql_check_active_connections(handle, threshold_percentage: int = 85)
		handle: Object of type unSkript POSTGRESQL Connector.
		threshold_percentage: Optional, percentage of connections to consider as the threshold.


## Lego Input
This Lego takes inputs handle, threshold_connections.

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)