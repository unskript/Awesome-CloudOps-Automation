##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def rest_get_handle(handle) -> None:
    """
    rest_get_handle returns the REST handle.
    :rtype: REST handle.
    """
    return handle
