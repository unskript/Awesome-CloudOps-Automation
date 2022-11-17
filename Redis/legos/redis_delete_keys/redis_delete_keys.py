#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

import pprint
from beartype import beartype
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    pattern: str = Field(
        title='Pattern',
        description='Pattern for the searched keys')


def redis_delete_keys_printer(output) -> int:
    if output is None:
        return
    pprint.pprint("{} keys were deleted".format(output))


def redis_delete_keys(handle, pattern: str):
    """redis_delete_keys deleted the pattern matched keys.

       :type pattern: string
       :param pattern: Pattern for the searched keys.

       :rtype: Count of deleted keys.
    """
    result = 0
    try:
        for key in handle.scan_iter(pattern):
            result = handle.delete(key)
            result += result
    except Exception as e:
        print(e)
    return result
        
