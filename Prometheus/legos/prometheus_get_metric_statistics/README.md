[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>Get Prometheus Metric Statistics</h1>

## Description
This Lego Gets Prometheus Metric Statistics.


## Lego Details

    prometheus_get_metric_range_data( handle, promql_query: str, timeSince: int, step: str) 

        handle: Object of type unSkript PROMETHEUS Connector
        promql_query: This is a PromQL query, a few examples can be found at https://prometheus.io/docs/prometheus/latest/querying/examples/.
        timeSince: Starting from now, window (in seconds) for which you want to get the metric values for.
        promql_query: Query resolution step width in duration format or float number of seconds.

## Lego Input
This Lego takes four inputs handle, promql_query, timeSince and step. 

## Lego Output
Here is a sample output.
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)