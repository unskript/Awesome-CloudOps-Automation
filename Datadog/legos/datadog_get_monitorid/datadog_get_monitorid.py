##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
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
    monitor_response = handle.Monitor.get_all(name=name)
    monitor_id = None
    if len(monitor_response) > 0:
        for monitor in monitor_response:
            if monitor["name"] == name:
                monitor_id = monitor["id"]
                break

    if not monitor_id:
        raise Exception("No monitor named {} found".format(name))
    
    return monitor_id
