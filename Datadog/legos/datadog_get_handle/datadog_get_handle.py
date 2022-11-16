##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def datadog_get_handle(handle):
    """datadog_get_handle returns the Datadog handle.

       :rtype: Datadog Handle.
    """
    return handle
