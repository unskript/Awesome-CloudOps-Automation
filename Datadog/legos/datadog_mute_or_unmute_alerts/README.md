[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Datadog get monitorID</h2>

<br>

## Description
This Lego Get monitorID given the name.


## Lego Details
    datadog_mute_or_unmute_alerts(handle: object, monitorIDs: List[int], all: bool, mute: bool,
                                  scope: str)

        handle: Object of type unSkript datadog Connector
        monitorIDs: List of monitor Ids to be modified. eg: [1643815305,1643815323]
        all: Set this to True if mute/unmute all monitors.
        mute: True to mute, False to unmute.
        scope: The scope to apply the mute to. For example, if your alert is grouped by "host", you might mute "host:app1".

## Lego Input
This Lego take five inputs handle, monitorIDs, all, mute and scope.

## Lego Output
Here is a sample output.


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)