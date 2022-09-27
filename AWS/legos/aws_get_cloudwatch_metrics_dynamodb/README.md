[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>AWS Get Cloudwatch Metrics DynamoDB </h1>

## Description
This Lego gives the AWS Cloudwatch Metrics for DynamoDB.


## Lego Details

    aws_get_cloudwatch_metrics_dynamodb(hdl: object, metric_name: DynamoDBMetrics, dimensions: List[dict], timeSince: int, statistics: StatisticsType, region: str, period: int)

        hdl: Object of type unSkript AWS Connector
        metric_name: The name of the metric, with or without spaces.
        dimensions: A dimension is a name/value pair that is part of the identity of a metric.
        period: The granularity, in seconds, of the returned data points.
        timeSince: Starting from now, window (in seconds) for which you want to get the datapoints for.
        statistics: Cloudwatch metric statistics. Possible values: SampleCount, Average, Sum, Minimum, Maximum.
        region: AWS Region of the cloudwatch.


## Lego Input
This Lego take seven inputs hdl, metric_name, dimensions, period, timeSince, statistics and region.


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://unskript.com)