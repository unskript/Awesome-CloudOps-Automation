#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

from typing import Optional, Tuple
from pydantic import BaseModel, Field
from tabulate import tabulate

class InputSchema(BaseModel):
    size_in_bytes: Optional[int] = Field(
        500,
        title='Size in Bytes',
        description='Threshold Size of Key in Bytes')


def redis_list_large_keys_printer(output):
    status, data = output

    if status:
        print("There are no large keys")
        return
    else:
        flattened_data = []
        for item in data:
            for key, value in item.items():
                flattened_data.append([key.decode(), value])

        headers = ["Key Name", "Key Size (Bytes)"]

        print("Large keys:")
        print(tabulate(flattened_data, headers=headers, tablefmt="grid"))



def redis_list_large_keys(handle, size_in_bytes: int = 500) -> Tuple :
    """redis_list_large_keys returns deleted stale keys greater than given a threshold time

       :type size_in_bytes: int
       :param size_in_bytes: Threshold Size of Key in Bytes

       :rtype: Dict of Large keys 
    """
    try:
        result = []
        large_keys = {}
        keys = handle.keys('*')
        for key in keys:
            value = handle.memory_usage(key)
            if value > int(size_in_bytes):
                large_keys[key]= value
                result.append(large_keys)
    except Exception as e:
        raise e
    if result:
        return (False, result)
    return (True, None)
