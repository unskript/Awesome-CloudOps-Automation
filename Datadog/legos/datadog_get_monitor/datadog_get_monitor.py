##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    monitor_id: int = Field(
        title='Monitor ID',
        description='ID of the monitor')

def datadog_get_monitor_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def datadog_get_monitor(handle,
                        monitor_id: int) -> Dict:
    """datadog_get_monitor gets the details for a monitor.

        :type monitor_id: int
        :param monitor_id: The ID of the monitor.

        :rtype: Dict of monitor details
    """
    try:
        with ApiClient(handle.handle_v2) as api_client:
            api_instance = MonitorsApi(api_client)
            monitor_details = api_instance.get_monitor(monitor_id=int(monitor_id))
    except Exception as e:
        raise e
    return monitor_details.to_dict()
