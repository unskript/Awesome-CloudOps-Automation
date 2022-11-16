##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def azure_get_handle(handle):
    """azure_get_handle returns the azure handle.

       :rtype: Azure Handle.
    """
    return handle
