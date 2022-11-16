##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def mantishub_get_handle(handle):
    """ mantishub_get_handle returns the Mantishub handle.

        :type handle: object
        :param handle: Object returned from task.validate(...).
        
        :rtype: Mantishub handle.
    """
    return handle
