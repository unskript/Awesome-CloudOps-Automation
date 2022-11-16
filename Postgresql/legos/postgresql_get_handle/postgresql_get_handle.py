##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel

class InputSchema(BaseModel):
    pass

def postgresql_get_handle(handle):
  """postgresql_get_handle returns the postgresql connection handle.
    :type handle: object
    :param handle: Object returned from task.validate(...).
    
    :rtype: postgresql Handle.
  """
  return handle
