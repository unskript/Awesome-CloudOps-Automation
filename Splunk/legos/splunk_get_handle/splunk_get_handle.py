##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def splunk_get_handle(handle):
    """splunk_get_handle returns the splunk handle.

       :rtype: splunk handle.
    """
    return handle
