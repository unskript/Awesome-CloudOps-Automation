##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
import datetime
from datetime import timedelta
from typing import Dict, Optional
from pydantic import BaseModel, Field
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi


class InputSchema(BaseModel):
    from_time: int = Field(
        title='From time',
        description='The time from which the metrics should be returned in seconds. Ex: 3600')
    tag_filter: Optional[str] = Field(
        title='Tag Filter',
        description=('Filter metrics that have been submitted with the given tags. Supports '
                     'boolean and wildcard expressions.Cannot be combined with other filters.')
                     )

def datadog_list_active_metrics_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def datadog_list_active_metrics(handle,
                                from_time: int,
                                tag_filter: str = "") -> Dict:
    """datadog_list_active_metrics get the list of actively reporting metrics from a 
       given time until now.

         :type from_time: int
        :param from_time: The time from which the metrics should be returned in seconds. Ex: 3600

        :type tag_filter: str
        :param tag_filter: Filter metrics that have been submitted with the given tags. 
        Supports boolean and wildcard expressions.Cannot be combined with other filters.

        :rtype: Dict of active metrics.
    """
    time_delta = datetime.datetime.utcnow() - timedelta(seconds=int(from_time))
    from_epoch = int(time_delta.timestamp())
    try:
        with ApiClient(handle.handle_v2) as api_client:
            api_instance = MetricsApi(api_client)
            metrics = api_instance.list_active_metrics(_from=from_epoch, tag_filter=tag_filter)
    except Exception as e:
        raise e
    return metrics.to_dict()
