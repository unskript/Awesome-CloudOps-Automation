##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass

def k8s_get_handle(handle):
  """kubernetes_get_handle returns the kubernetes handle.

     :rtype: kubernetes Handle.
  """
  return handle
