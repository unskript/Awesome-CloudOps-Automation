##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datetime import datetime, timedelta
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    from_time: int = Field(
        title='From time',
        description='Start of the queried time period in seconds. Ex: 3600')
    to_time: int = Field(
        title='From time',
        description='End of the queried time period in seconds. Ex: 3600')
    query: str = Field(
        title='Query String',
        description='Query string. Ex: system.cpu.idle{*}')

def datadog_query_metrics_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def datadog_query_metrics(handle,
                        from_time: int,
                        to_time: int,
                        query: str) -> Dict:
    """datadog_query_metrics queries timeseries points for a metric.

         :type from_time: int
        :param from_time: The time from which the metrics should be returned in seconds. Ex: 3600

        :type to_time: int
        :param to_time: The time until which the metrics should be returned in seconds. Ex: 3600

        :type query: str
        :param query: Query string. Ex: system.cpu.idle{*}

        :rtype: Dict of queried metric
    """
    try:
        with ApiClient(handle) as api_client:
            api_instance = MetricsApi(api_client)
            response = api_instance.query_metrics(
                _from=int((datetime.utcnow() - timedelta(seconds=int(from_time))).timestamp()),
                to=int((datetime.utcnow() - timedelta(seconds=int(to_time))).timestamp()),
                query=query,
            )
    except Exception as e:
        raise e
    return response.to_dict()
