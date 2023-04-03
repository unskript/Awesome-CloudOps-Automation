[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Kafka Check In-Sync Replicas</h2>

<br>

## Description
This Lego Checks number of actual min-isr for each topic-partition with configuration for that topic.


## Lego Details

    kafka_check_in_sync_replicas(handle: object, min_isr: int)

        handle: Object of type unSkript kafka Connector
        min_isr: Default min.isr value for cases without settings in Zookeeper. The default value is 3.

## Lego Input
This Lego take two input handle, and min_isr.

## Lego Output
Here is a sample output.


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)