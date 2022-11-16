##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def prometheus_get_handle(handle):
    """prometheus_get_handle returns the prometheus api connection handle.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :rtype: prometheus Handle.
    """
    return handle
