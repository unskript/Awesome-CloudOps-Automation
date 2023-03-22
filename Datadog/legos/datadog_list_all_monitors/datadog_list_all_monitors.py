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
        with ApiClient(handle.handle_v2) as api_client:
            api_instance = MonitorsApi(api_client)
            monitors = []
            page = 0
            while True:
                response = api_instance.list_monitors(page_size=30,page=page)
                if response == []:
                    break
                monitors.extend(response)
                page += 1
    except Exception as e:
        raise e
    return monitors

