#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

import pprint
from typing import Dict
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    time_in_sec: int = Field(
        title='Time in Seconds',
        description='Threshold Idle Time in Seconds')


def redis_delete_stale_keys(output):
    if output is None:
        return
    print("Deleted Keys: ")
    pprint.pprint(output)


def redis_delete_stale_keys(handle, time_in_sec: int) -> Dict :
    """redis_delete_stale_keys returns deleted stale keys greater than given a threshold time

       :type time_in_sec: int
       :param time_in_sec: Threshold Idle Time in Seconds

       :rtype: Dict of Deleted Unused keys 
    """
    try:
        result = {}
        for key in handle.scan_iter("*"):
            idle_time = handle.object("idletime", key)
            if idle_time > time_in_sec:
                result[key]= idle_time
                handle.delete(key)
    except Exception as e:
        result["error"] = e
    return result
