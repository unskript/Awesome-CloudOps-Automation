[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Datadog list active metrics</h2>

<br>

## Description
This Lego lists all active metrics in datadog.


## Lego Details
    datadog_list_active_metrics(handle,
                                from_time: int,
                                tag_filter: str = "") -> Dict:
        from_time: The time from which the metrics should be returned in seconds. Ex: 3600
        tag_filter: Filter metrics that have been submitted with the given tags. Supports boolean and wildcard expressions.Cannot be combined with other filters.
        handle: Object of type unSkript datadog Connector

## Lego Input
This Lego take 3 inputs handle, from_time, tag_filter

## Lego Output
Here is a sample output.


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)