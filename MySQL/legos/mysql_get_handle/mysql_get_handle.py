##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def mysql_get_handle(handle):
    """mysql_get_handle returns the mysql connection handle.

       :rtype: mysql Handle.
    """
    return handle
