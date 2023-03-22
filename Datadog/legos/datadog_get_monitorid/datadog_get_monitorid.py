##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client import ApiClient
from datadog_api_client.exceptions import NotFoundException
import pprint

class InputSchema(BaseModel):
    name: str = Field(
        title='name',
        description='Name of the target monitor.')

def datadog_get_monitorid_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def datadog_get_monitorid(handle, name: str) -> int:
    """datadog_get_monitorid gets monitor id.

        :type name: str
        :param name: Name of the target monitor.

        :rtype: The monitor id.
    """
    try:
        with ApiClient(handle.handle_v2) as api_client:
            api_instance = MonitorsApi(api_client)
            monitors = []
            page = 0
            while True:
                response = api_instance.list_monitors(page_size=30, page=page, name=name)
                if response == []:
                    break
                monitors.extend(response)
                page += 1
    except Exception as e:
        raise e
    if len(monitors) == 1:
        return int(monitors[0]['id'])
    else:
        raise NotFoundException
