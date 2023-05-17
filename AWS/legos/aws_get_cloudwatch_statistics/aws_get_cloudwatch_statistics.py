##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import pprint
from typing import Optional, List
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import matplotlib.pyplot as plt
from unskript.legos.aws.aws_get_handle.aws_get_handle import Session
from unskript.enums.aws_k8s_enums import StatisticsType
from tabulate import tabulate


class InputSchema(BaseModel):
    name_space: str = Field(
        title="Namespace",
        description="The namespace of the metric, with or without spaces. For eg: AWS/SQS, AWS/ECS",
    )
    metric_name: str = Field(
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


def aws_get_cloudwatch_statistics_printer(output):
    if output is None:
        return
    plt.show()
    pprint.pprint(output)


def aws_get_cloudwatch_statistics(
    hdl: Session,
    name_space: str,
    metric_name: str,
    dimensions: List[dict],
    timeSince: int,
    statistics: StatisticsType,
    region: str,
    period: int = 60,
) -> str:
    """aws_get_cloud_statistics shows ploted AWS cloudwatch statistics.
    for a given instance ID. This routine assume instance_id
    being present in the inputParmsJson.

        :type name_space: string
        :param name_space: he namespace of the metric, with or without spaces.
        For eg: AWS/SQS, AWS/ECS

        :type metric_name: string
        :param metric_name: The name of the metric, with or without spaces.

        :type dimensions: List[dict]
        :param dimensions: A dimension is a name/value pair that is part of the
        identity of a metric.

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

        :rtype: Shows ploted statistics.
    """
    statistics = statistics.value if statistics else None
    cloudwatchClient = hdl.client("cloudwatch", region_name=region)
    # Gets metric statistics.
    res = cloudwatchClient.get_metric_statistics(
        Namespace=name_space,
        MetricName=metric_name,
        Dimensions=dimensions,
        Period=period,
        StartTime=datetime.utcnow() - timedelta(seconds=timeSince),
        EndTime=datetime.utcnow(),
        Statistics=[statistics],
    )

    data = {}
    table_data = []
    for datapoints in res["Datapoints"]:
        data[datapoints["Timestamp"]] = datapoints[statistics]

    # Sorts data.
    data_keys = data.keys()
    times_stamps = list(data_keys)
    times_stamps.sort()
    sorted_values = []
    for value in times_stamps:
        table_data.append([value, data[value]])
        sorted_values.append(data[value])
    head = ["Timestamp", "Value"]
    table = tabulate(table_data, headers=head, tablefmt="grid")
    # Puts datapoints into the plot.
    plt.plot_date(times_stamps, sorted_values, "-o")

    return table
