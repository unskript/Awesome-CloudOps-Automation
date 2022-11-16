##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel
from typing import List

class InputSchema(BaseModel):
    pass


def prometheus_get_all_metrics_printer(output):
    if output is None:
        return
    for metric in output:
        print(metric)


def prometheus_get_all_metrics(handle) -> List:
    """prometheus_get_all_metrics Returns Prometheus Metrics.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :return: Metrics list.
    """
    return handle.all_metrics()
