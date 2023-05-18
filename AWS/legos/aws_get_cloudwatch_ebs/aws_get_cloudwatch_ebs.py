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
from unskript.enums.aws_cloudwatch_enums import EBSMetrics
from unskript.enums.aws_k8s_enums import StatisticsType
from tabulate import tabulate


class InputSchema(BaseModel):
    volumes: List[str] = Field(
        title="Volume",
        description="List of EBS volumes",
    )
    metric_name: EBSMetrics = Field(
        title="Metric",
        description=("The name of the EBS metric. Eg VolumeReadBytes|VolumeWriteBytes|VolumeReadOps"
                     "|VolumeWriteOps|VolumeTotalReadTime|VolumeTotalWriteTime|VolumeIdleTime"
                     "|VolumeQueueLength|VolumeThroughputPercentage|VolumeConsumedReadWriteOps|BurstBalance")
    )
    period: Optional[int] = Field(
        default=60,
        title="Period",
        description="The granularity, in seconds, of the returned data points.",
    )
    timeSince: int = Field(
        default=3600,
        title="Time Since",
        description=("Starting from now, window (in seconds) for which you want to get"
                     " the datapoints for.")
    )
    statistics: StatisticsType = Field(
        title="Statistics",
        description=("Cloudwatch metric statistics. Possible values: "
                     "SampleCount, Average, Sum, Minimum, Maximum.")
    )
    region: str = Field(
        title="Region",
        description="AWS Region of the cloudwatch.")


def aws_get_cloudwatch_ebs_printer(output):
    if output is None:
        return
    plt.show()
    pprint.pprint(output)


def aws_get_cloudwatch_ebs(
    hdl: Session,
    metric_name: EBSMetrics,
    volumes: List[str],
    region: str,
    timeSince: int,
    statistics: StatisticsType,
    period: int = 60,
) -> str:

    """aws_get_cloudwatch_ebs shows plotted AWS cloudwatch statistics for ebs.

        :type metric_name: ApplicationELBMetrics
        :param metric_name: The name of the metric, with or without spaces.

        :type volumes: List[str]
        :param volumes: List of EBS volumes

        :type period: int
        :param period: The granularity, in seconds, of the returned data points.

        :type timeSince: int
        :param timeSince: Starting from now, window (in seconds) for which you
        want to get the datapoints for.

        :type statistics: StatisticsType
        :param statistics: Cloudwatch metric statistics. Possible values: SampleCount,
        Average, Sum, Minimum, Maximum.

        :type region: string
        :param region: AWS Region of the cloudwatch.

        :rtype: Shows ploted statistics.
    """
    metric_name = metric_name.value if metric_name else None
    statistics = statistics.value if statistics else None
    cloudwatchClient = hdl.client("cloudwatch", region_name=region)

    name_space = "AWS/EBS"
    dimensions = [{"Name": "VolumeId", "Value": v}
                  for v in volumes]

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
    for datapoints in res["Datapoints"]:
        data[datapoints["Timestamp"]] = datapoints[statistics]

    # Sorts data.
    data_keys = data.keys()
    times_stamps = list(data_keys)
    times_stamps.sort()
    sorted_values = []
    table_data = []
    for value in times_stamps:
        table_data.append([value, data[value]])
        sorted_values.append(data[value])
    head = ["Timestamp", "Value"]
    table = tabulate(table_data, headers=head, tablefmt="grid")
    # Puts datapoints into the plot.
    plt.plot_date(times_stamps, sorted_values, "-o")

    return table
