##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def opensearch_get_handle(handle):
    """
    opensearch_get_handle returns the Opensearch handle.
    :rtype: Opensearch handle.
    """
    return handle
