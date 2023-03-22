[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Datadog query metrics</h2>

<br>

## Description
This Lego queries timeseries points for a metric.


## Lego Details
    datadog_query_metrics(handle,
                                from_time: int,
                                to_time: int,
                                query: str) -> Dict:
        query: Query string. Ex: system.cpu.idle{*}
        from_time: The time from which the metrics should be returned in seconds. Ex: 3600
        to_time: The time until which the metrics should be returned in seconds. Ex: 3600
        handle: Object of type unSkript datadog Connector

## Lego Input
This Lego take 4 inputs handle, from_time, to_time, query

## Lego Output
Here is a sample output.


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)