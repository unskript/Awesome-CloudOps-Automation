##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def mongodb_get_handle(handle):
    """mongodb_get_handle returns the mongo client.
    
        :type handle: object
        :param handle: Object returned from task.validate(...).

        :rtype: mongo client.
    """
    return handle
