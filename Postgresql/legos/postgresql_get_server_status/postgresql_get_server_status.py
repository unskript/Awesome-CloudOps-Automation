##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from typing import Tuple
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def postgresql_get_server_status_printer(output):
    if output[0]:
        print("PostgreSQL Server Status: Reachable")
    else:
        error_message = output[1]['message'] if output[1] else "Unknown error"
        print("PostgreSQL Server Status: Unreachable")
        print(f"Error: {error_message}")

def postgresql_get_server_status(handle) -> Tuple:
    """
    Returns a simple status indicating the reachability of the PostgreSQL server.

    :type handle: object
    :param handle: PostgreSQL connection object

    :return: Tuple containing a boolean indicating success and optional error message
    """
    try:
        cur = handle.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        return (True, None)
    except Exception as e:
        return (False, {"message": str(e)})
    finally:
        handle.close()


