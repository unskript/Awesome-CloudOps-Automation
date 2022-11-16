##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def ssh_get_handle(handle):
    """
    ssh_get_handle returns the SSH handle.
       :rtype: SSH handle.
    """
    return handle
