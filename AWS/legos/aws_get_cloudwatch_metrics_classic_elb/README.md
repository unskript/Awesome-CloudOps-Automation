[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>Get AWS CloudWatch Metrics for AWS/ELB</h1>

## Description
This Lego get AWS CloudWatch Metrics for Classic Loadbalancer.


## Lego Details

    aws_get_cloudwatch_ebs(hdl: Session, metric_name: ClassicELBMetrics, dimensions: List[dict], region: str, timeSince: int,statistics: StatisticsType, period: int)

        hdl: Object of type unSkript AWS Connector.
        metric_name: The name of the metric
        dimensions: A dimension is a name/value pair that is part of the identity of a metric.
        timeSince: Starting from now, window (in seconds) for which you want to get the datapoints for.
        statistics: Cloudwatch metric statistics.
        period: The granularity, in seconds, of the returned data points.
        units: Unit of measure.
        region: AWS Region of the cloudwatch.

## Lego Input

This Lego take eight inputs hdl, metric_name, dimensions, timeSince, statistics, period, units and region.


## Lego Output
Here is a sample output.
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)