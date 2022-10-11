##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def gcp_get_handle(handle):
    """gcp_get_handle returns the GCP handle.

       :rtype: GCP Handle.
    """
    return handle
