[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Schedule downtime</h2>

<br>

## Description
This Lego used to Schedule downtime.


## Lego Details
    datadog_schedule_downtime(handle: object, duration: int, scope:list, monitor_id: int,
                              monitor_tags:list)

        handle: Object of type unSkript datadog Connector
        duration: Select a duration in minutes eg: 60.
        scope: The scope(s) to which the downtime applies.
        monitor_id: A single monitor to which the downtime applies. If not provided, the downtime applies to all monitors.
        monitor_tags: A comma-separated list of monitor tags.

## Lego Input
This Lego take five inputs handle, duration, scope, monitor_id and monitor_tags.

## Lego Output
Here is a sample output.


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)