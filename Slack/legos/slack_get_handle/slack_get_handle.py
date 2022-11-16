##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def slack_get_handle(handle) -> None:
    """slack_get_handle returns the slack handle.

       :rtype: slack Handle.
    """
    return handle
