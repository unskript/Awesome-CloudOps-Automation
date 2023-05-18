##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel

class InputSchema(BaseModel):
    pass


def jenkins_get_handle(handle):
    """jenkins_get_handle returns the jenkins server handle.

          :rtype: Jenkins handle.
    """
    return handle
