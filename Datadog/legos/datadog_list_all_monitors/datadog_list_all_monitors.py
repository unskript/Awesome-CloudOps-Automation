##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List

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
    metadata = handle.Monitor.search()["metadata"]
    monitors = []
    total_no_pages = metadata.get("page_count")
    for page in range(0, total_no_pages):
        monitor_response = handle.Monitor.get_all(page=page)
        monitors.extend(monitor_response)
    return monitors
