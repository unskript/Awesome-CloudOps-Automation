##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def salesforce_get_handle(handle) -> None:
    """
    salesforce_get_handle returns the Salesforce handle.
    :rtype: Salesforce handle.
    """
    return handle
