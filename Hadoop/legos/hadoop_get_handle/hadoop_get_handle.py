##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel

class InputSchema(BaseModel):
    pass


def hadoop_get_handle(handle) -> None:
    """hadoop_get_handle returns the Hadoop session handle.
       :rtype: Hadoop handle.
    """
    return handle
