##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def elasticsearch_get_handle(handle):
    """elasticsearch_get_handle returns the elasticsearch client handle.

       :rtype: elasticsearch client handle.
    """
    return handle
