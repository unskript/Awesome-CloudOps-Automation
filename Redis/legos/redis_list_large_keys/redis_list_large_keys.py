#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

import pprint
from typing import Dict
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    size_in_bytes: int = Field(
        title='Size in Bytes',
        description='Threshold Size of Key in Bytes')


def redis_list_large_keys_printer(output):
    if output is None:
        print("There are no large keys")
        return
    pprint.pprint(output)


def redis_list_large_keys(handle, size_in_bytes: int) -> Dict :
    """redis_list_large_keys returns deleted stale keys greater than given a threshold time

       :type size_in_bytes: int
       :param size_in_bytes: Threshold Size of Key in Bytes

       :rtype: Dict of Large keys 
    """
    try:
        result = {}
        keys = handle.keys('*')
        for key in keys:
            value = handle.memory_usage(key)
            if value > int(size_in_bytes):
                result[key]= value
    except Exception as e:
        result["error"] = e
    return result
