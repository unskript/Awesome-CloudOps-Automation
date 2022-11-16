##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from tabulate import tabulate
from unskript.legos.aws.aws_get_handle.aws_get_handle import Session
from unskript.enums.aws_cloudwatch_enums import ApplicationELBMetrics
from unskript.enums.aws_k8s_enums import StatisticsType
import pprint


class InputSchema(BaseModel):
    metric_name: ApplicationELBMetrics = Field(
        title="Metric Name",
        description="The name of the metric, with or without spaces.",
    )
    dimensions: List[dict] = Field(
        title="Dimensions",
        description="A dimension is a name/value pair that is part of the identity of a metric.",
    )
    period: Optional[int] = Field(
        60,
        title="Period",
        description="The granularity, in seconds, of the returned data points.",
    )
    timeSince: int = Field(
        title="Time Since",
        description="Starting from now, window (in seconds) for which you want to get the datapoints for.",
    )
    statistics: StatisticsType = Field(
        title="Statistics",
        description="Cloudwatch metric statistics. Possible values: Average, Sum, Minimum, Maximum.",
    )
    region: str = Field(
        title="Region", description="AWS Region of the cloudwatch.")


def aws_get_cloudwatch_metrics_applicationelb_printer(output):
    if output is None:
        return
    plt.show()
    pprint.pprint(output)


def aws_get_cloudwatch_metrics_applicationelb(
    hdl: Session,
    metric_name: ApplicationELBMetrics,
    dimensions: List[dict],
    timeSince: int,
    statistics: StatisticsType,
    region: str,
    period: int = 60,
) -> str:
    """aws_get_cloudwatch_metrics_applicationelb shows plotted AWS cloudwatch statistics for Application ELB.

        :type metric_name: ApplicationELBMetrics
        :param metric_name: The name of the metric, with or without spaces.

        :type dimensions: List[dict]
        :param dimensions: A dimension is a name/value pair that is part of the identity of a metric.

        :type period: int
        :param period: The granularity, in seconds, of the returned data points.

        :type timeSince: int
        :param timeSince: Starting from now, window (in seconds) for which you want to get the datapoints for.

        :type statistics: StatisticsType
        :param statistics: Cloudwatch metric statistics. Possible values: SampleCount, Average, Sum, Minimum, Maximum.

        :type region: string
        :param region: AWS Region of the cloudwatch.

        :rtype: Shows ploted statistics.
    """
    metric_name = metric_name.value if metric_name else None
    statistics = statistics.value if statistics else None
    cloudwatchClient = hdl.client("cloudwatch", region_name=region)
    # Gets metric data.
    res = cloudwatchClient.get_metric_data(
        MetricDataQueries=[
            {
                'Id': metric_name.lower(),
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': metric_name,
                        'Dimensions': dimensions
                    },
                    'Period': period,
                    'Stat': statistics,
                },
            },
        ],
        StartTime=datetime.utcnow() - timedelta(seconds=timeSince),
        EndTime=datetime.utcnow(),
        ScanBy='TimestampAscending'
    )

    timestamps = []
    values = []

    for timestamp in res['MetricDataResults'][0]['Timestamps']:
        timestamps.append(timestamp)
    for value in res['MetricDataResults'][0]['Values']:
        values.append(value)

    timestamps.sort()
    values.sort()

    plt.plot_date(timestamps, values, "-o")

    data = []
    for dt, val in zip(res['MetricDataResults'][0]['Timestamps'], res['MetricDataResults'][0]['Values']):
        data.append([dt.strftime('%Y-%m-%d::%H-%M'), val])
    head = ["Timestamp", "Value"]
    table = tabulate(data, headers=head, tablefmt="grid")

    return table
