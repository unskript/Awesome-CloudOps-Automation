##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client import ApiClient
from typing import Dict, Optional
import pprint

class InputSchema(BaseModel):
    query: Optional[str] = Field(
        "",
        title='Query',
        description='Query string to list metrics upon. Can optionally be prefixed with ``metrics:``. By default all metrics are returned')

def datadog_list_metrics_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def datadog_list_metrics(handle, query: str = "") -> Dict:
    """datadog_list_metrics lists metrics from the last 24 hours in Datadog.

        :type name: str
        :param query: Query string to list metrics upon. Can optionally be prefixed with ``metrics:``.

        :rtype: A Dict containing the queried metrics
    """
    try:
        with ApiClient(handle.handle_v2) as api_client:
            api_instance = MetricsApi(api_client)
            metrics = api_instance.list_metrics(q=query)
    except Exception as e:
        raise e
    return metrics.to_dict()