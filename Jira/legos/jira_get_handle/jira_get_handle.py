##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def jira_get_handle(handle):
    """jira_get_handle returns the jira connection handle.

       :rtype: postgresql Handle.
    """
    return handle
