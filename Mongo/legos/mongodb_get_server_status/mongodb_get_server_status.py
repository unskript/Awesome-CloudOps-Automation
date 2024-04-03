##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from tabulate import tabulate


class InputSchema(BaseModel):
    pass



def mongodb_get_server_status_printer(output):
    if output[0]:
        print("MongoDB Server Status: Reachable")
    else:
        print("MongoDB Server Status: Unreachable")
        if output[1]:
            print(f"Error: {output[1]}")

def mongodb_get_server_status(handle) -> Tuple:
    """Returns the status of the MongoDB instance.

    :type handle: object
    :param handle: MongoDB connection object

    :return: Status indicating server reachability of mongo server
    """
    try:
        # Check server reachability
        result = handle.admin.command("ping")
        if result and result.get("ok"):
            return (True, None)
    except Exception as e:
        return (False, str(e))
    return (False, "Unable to check Mongo server status")
