##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import pprint
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import matplotlib.pyplot as plt
from tabulate import tabulate
from unskript.legos.aws.aws_get_handle.aws_get_handle import Session
from unskript.enums.aws_k8s_enums import StatisticsType
from unskript.enums.aws_cloudwatch_enums import LambdaMetrics


class InputSchema(BaseModel):
    metric_name: LambdaMetrics = Field(
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
        description=("Starting from now, window (in seconds) for which you want "
                     "to get the datapoints for.")
    )
    statistics: StatisticsType = Field(
        title="Statistics",
        description=("Cloudwatch metric statistics. Possible values: SampleCount, "
                     "Average, Sum, Minimum, Maximum.")
    )
    region: str = Field(
        title="Region", description="AWS Region of the cloudwatch.")


def aws_get_cloudwatch_metrics_lambda_printer(output) -> str:
    if output is None:
        return ""
    if isinstance(output, Dict):
        for key in output:
            plt.plot_date(output[key][0], output[key][1], "-o")
            pprint.pprint(output[key][2])
            plt.show()
    else:
        plt.plot_date(output[0], output[1], "-o")
        pprint.pprint(output[2])
        plt.show()
    return None



def aws_get_cloudwatch_metrics_lambda(
    hdl: Session,
    metric_name: LambdaMetrics,
    dimensions: List[dict],
    timeSince: int,
    statistics: StatisticsType,
    region: str,
    period: int = 60,
) -> List:
    """get_lambda_metrics shows plotted AWS cloudwatch statistics for Lambda.

        :type metric_name: LambdaMetrics
        :param metric_name: The name of the metric, with or without spaces.

        :type dimensions: List[dict]
        :param dimensions: A dimension is a name/value pair that is part of
        the identity of a metric.

        :type period: int
        :param period: The granularity, in seconds, of the returned data points.

        :type timeSince: int
        :param timeSince: Starting from now, window (in seconds) for which you want
        to get the datapoints for.

        :type statistics: StatisticsType
        :param statistics: Cloudwatch metric statistics. Possible values: SampleCount,
        Average, Sum, Minimum, Maximum.

        :type region: string
        :param region: AWS Region of the cloudwatch.

        :rtype: Shows plotted statistics.
    """
    result = []
    cloudwatch_client = hdl.client("cloudwatch", region_name=region)
    statistics = statistics.value if statistics else None
    metric_name = metric_name.value if metric_name else None
    # Gets metric data.
    res = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': metric_name.lower(),
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/Lambda',
                        'MetricName': metric_name,
                        'Dimensions': dimensions
                    },
                    'Period': period,
                    'Stat': statistics
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

    data = []
    for dt,val in zip(
        res['MetricDataResults'][0]['Timestamps'],
        res['MetricDataResults'][0]['Values']
        ):
        data.append([dt.strftime('%Y-%m-%d::%H-%M'), val])
    head = ["Timestamp", "Value"]
    table = tabulate(data, headers=head, tablefmt="grid")
    result.append(timestamps)
    result.append(values)
    result.append(table)
    return result
