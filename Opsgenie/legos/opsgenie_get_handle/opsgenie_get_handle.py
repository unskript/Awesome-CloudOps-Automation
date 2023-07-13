##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass



def opsgenie_get_handle_printer(output):
    if output is None:
        return
    print(output)

def opsgenie_get_handle(handle):
    """opsgenie_get_handle returns the nomad handle.

          :rtype: Opsgenie handle.
    """
    return handle



