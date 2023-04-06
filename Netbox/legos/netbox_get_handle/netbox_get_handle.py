##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def netbox_get_handle(handle):
    """netbox_get_handle returns the nomad handle.

          :rtype: Nomad handle.
    """
    return handle
