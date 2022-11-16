##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def mongodb_get_server_status_printer(output):
    if output is None:
        return
    print("\n\n")
    pprint.pprint(output)
    return output


def mongodb_get_server_status(handle) -> Dict:
    """mongodb_get_server_status returns the mongo server status.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :rtype: Dict with server status.
    """
    try:
        res = handle.admin.command("serverStatus")
        return res
    except Exception as e:
        return {"Error": e}
