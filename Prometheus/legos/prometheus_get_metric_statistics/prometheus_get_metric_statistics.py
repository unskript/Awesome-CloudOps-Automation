##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import pprint
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pydantic import BaseModel, Field
from tabulate import tabulate


class InputSchema(BaseModel):
    promql_query: str = Field(
        title="PromQL Query",
        description="This is a PromQL query, a few examples can be found at \
            https://prometheus.io/docs/prometheus/latest/querying/examples/"
    )
    timeSince: int = Field(
        title="Time Since",
        description="Starting from now, window (in seconds) \
            for which you want to get the datapoints for.",
    )
    step: str = Field(
        title="Step",
        description="Query resolution step width in duration format or float number of seconds.",
    )
    graph_size: list = Field(
        default=[10, 5],
        title="Graph Size",
        description="Size of the graph in inches (width, height), specified as a list.",
    )


def prometheus_get_metric_range_data_printer(output):
    if output is None:
        return
    plt.show()
    pprint.pprint(output)


def prometheus_get_metric_range_data(
    handle,
    promql_query: str,
    timeSince: int,
    step: str,
    graph_size: list = [10, 5]
) -> str:
    """prometheus_get_metric_statistics shows plotted values of Prometheus metric statistics.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :type promql_query: string
    :param PromQL Query: This is a PromQL query, a few examples can be found at 
    https://prometheus.io/docs/prometheus/latest/querying/examples/

    :type timeSince: int
    :param timeSince: Starting from now, window (in seconds) for which you want
    to get the metric values for.

    :type step: string
    :param Step: Query resolution step width in duration format or float number of seconds

    :type graph_size: list
    :param graph_size: Size of the graph in inches (width, height), specified as a list.

    :rtype: Shows plotted statistics.
    """
    result = handle.custom_query_range(
        query=promql_query,
        start_time=datetime.utcnow() - timedelta(seconds=timeSince),
        end_time=datetime.utcnow(),
        step=step)
    data = []
    table_data = []
    plt.figure(figsize=graph_size)
    for each_result in result:
        metric_data = {}
        for each_metric_value in each_result["values"]:
            metric_data[datetime.fromtimestamp(each_metric_value[0])] = each_metric_value[1]
        data.append(metric_data)
    for metric_values in data:
        data_keys = metric_values.keys()
        times_stamps = list(data_keys)
        times_stamps.sort()
        sorted_values = []
        for time in times_stamps:
            table_data.append([time, metric_values[time]])
            sorted_values.append(metric_values[time])
        plt.plot_date(times_stamps, sorted_values, "-o")
    head = ["Timestamp", "Value"]
    table = tabulate(table_data, headers=head, tablefmt="grid")
    return table
