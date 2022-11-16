##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def mssql_get_handle(handle):
    """mssql_get_handle retuns the handle of MSSQL.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :rtype: handle of MSSQL.
      """
    return handle
