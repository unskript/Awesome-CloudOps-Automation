##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel
import json
import pprint

class InputSchema(BaseModel):
    pass

def datadog_list_all_monitors_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def datadog_list_all_monitors(handle) -> str:
    """datadog_get_all_monitors gets all monitors

        :rtype: The list of monitors as json.
    """
    monitor_response = handle.Monitor.get_all()
    if len(monitor_response) == 0:
        raise Exception("No monitors found")

    return json.dumps(monitor_response)
