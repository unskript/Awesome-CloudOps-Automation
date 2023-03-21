##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client import ApiClient
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass

def datadog_list_all_monitors_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def datadog_list_all_monitors(handle) -> List[dict]:
    """datadog_get_all_monitors gets all monitors

        :rtype: The list of monitors.
    """
    try:
        with ApiClient(handle) as api_client:
            api_instance = MonitorsApi(api_client)
            monitors = []
            total_no_pages = api_instance.search_monitors()['metadata']['page_count']
            for page in range(0, int(total_no_pages)):
                monitor_response = api_instance.search_monitors(page=page)
                monitors.extend(monitor_response['monitors'])
    except Exception as e:
        raise e
    return monitors

