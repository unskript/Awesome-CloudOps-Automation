[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>Get Pingdom Analysis Results for a specified Check</h1>

## Description
This Lego Returns Pingdom Analysis Results for a specified Check.


## Lego Details

    pingdom_get_analysis(handle, checkid: int, from_timestamp: int = 0, limit: int = 100, offset: int = 0, to_timestamp: int = 0)

        handle: Object of type unSkript PINGDOM Connector
        checkid: Pingdom Check ID.
        limit: Number of results to get.
        from_timestamp: Start Time Timestamp in the UNIX Format date.
        offset:Offset of returned checks.
        to_timestamp: End Time Timestamp in the UNIX Format date.


## Lego Input
This Lego take six inputs handle, checkid, limit,from_timestamp, to_timestamp and offset. 

## Lego Output
Here is a sample output.
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)