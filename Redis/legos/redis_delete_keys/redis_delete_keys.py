#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

import pprint
from typing import List
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    pattern: str = Field(
        title='Pattern',
        description='Pattern for the searched keys')


def redis_delete_keys_printer(output):
    if output is None:
        return
    pprint.pprint("Deleted Keys: ")
    pprint.pprint(output)


def redis_delete_keys(handle, pattern: str) -> List:
    """redis_delete_keys deleted the pattern matched keys.

       :type pattern: string
       :param pattern: Pattern for the searched keys.

       :rtype: List of deleted keys.
    """
    result = []
    try:
        for key in handle.scan_iter(pattern):
            result.append(key)
            handle.delete(key)
    except Exception as e:
        print(e)
    return result
