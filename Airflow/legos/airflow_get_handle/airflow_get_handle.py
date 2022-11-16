##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def airflow_get_handle(handle):
    """airflow_get_handle returns the airflow handle.

       :rtype: airflow Handle.
    """
    return handle
