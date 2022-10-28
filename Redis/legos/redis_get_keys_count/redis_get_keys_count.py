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

@beartype
def redis_get_keys_count_printer(output):
    if output is None:
        return
    pprint.pprint({"Matched keys count": output})

@beartype
def redis_get_keys_count(handle, pattern: str):
    """redis_get_keys_count returns the matched keys count.

       :type pattern: string
       :param pattern: Pattern for the searched keys.

       :rtype: Matched keys count.
    """

    output = 0
    for key in handle.scan_iter(pattern):
        output += 1

    return output
