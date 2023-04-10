##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def nomad_get_handle(handle):
    """nomad_get_handle returns the nomad handle.

          :rtype: Nomad handle.
    """
    return handle
