#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

import pprint
from beartype import beartype
from pydantic import BaseModel, Field
from typing import List

class InputSchema(BaseModel):
    pass


def redis_delete_all_keys_printer(output):
    if output is None:
        return
    pprint.pprint("Deleted Keys: ")
    pprint.pprint(output)


def redis_delete_all_keys(handle) -> List:
    """redis_delete_all_keys deleted the pattern matched keys.

       :rtype: List of all deleted keys.
    """
    result = []
    try:
        for key in handle.scan_iter('*'):
            result.append(key)
            handle.delete(key)
    except Exception as e:
        print(e)
    return result