[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>Get AWS CloudWatch Metrics for AWS/RDS </h1>

## Description
This Lego get AWS CloudWatch Metrics for AWS/RDS.


## Lego Details

    aws_get_cloudwatch_metrics_rds(hdl: Session, metric_name: RDSMetrics, dimensions: List[dict], region: str, timeSince: int,statistics: StatisticsType, period: int)

        hdl: Object of type unSkript AWS Connector.
        metric_name: The name of the metric, with or without spaces.
        dimensions: A dimension is a name/value pair that is part of the identity of a metric.
        timeSince: Starting from now, window (in seconds) for which you want to get the datapoints for.
        statistics: Cloudwatch metric statistics.
        period: The granularity, in seconds, of the returned data points.
        region: AWS Region of the cloudwatch.

## Lego Input

This Lego take seven inputs hdl, metric_name, dimensions, timeSince, statistics, period and region.


## Lego Output
Here is a sample output.
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)