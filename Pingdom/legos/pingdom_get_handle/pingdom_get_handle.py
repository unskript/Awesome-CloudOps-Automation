##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def pingdom_get_handle(handle):
    """pingdom_get_handle returns the Pingdom handle.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :rtype: Pingdom Handle.
    """
    return handle
