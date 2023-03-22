##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    metric_name: str = Field(
        title='Metric name',
        description='Name of the metric for which to get metadata.')

def datadog_get_metric_metadata_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def datadog_get_metric_metadata(handle,
                                metric_name: str) -> Dict:
    """datadog_get_metric_metadata gets the metadata for a metric.

        :type metric_name: str
        :param metric_name: Name of the metric for which to get metadata.

        :rtype: Dict of metadata of metric
    """
    try:
        with ApiClient(handle.handle_v2) as api_client:
            api_instance = MetricsApi(api_client)
            metric_metadata = api_instance.get_metric_metadata(metric_name=metric_name)
    except Exception as e:
        raise e
    return metric_metadata.to_dict()
