#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def redis_get_handle(handle):
    """redis_get_handle returns the Redis handle.

       :rtype: Redis Handle
    """
    return handle
