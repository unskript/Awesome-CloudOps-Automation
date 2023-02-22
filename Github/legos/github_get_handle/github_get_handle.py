##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def github_get_handle(handle):
    """github_get_handle returns the github handle.

          :rtype: Github handle.
    """
    return handle
