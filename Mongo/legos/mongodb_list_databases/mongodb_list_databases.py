##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel
from pymongo.errors import AutoReconnect, ServerSelectionTimeoutError


class InputSchema(BaseModel):
    pass


def mongodb_list_databases_printer(output):
    if output is None:
        return
    print("\n\n")
    pprint.pprint("List of databases")
    pprint.pprint(output)


def mongodb_list_databases(handle) -> List:
    """mongodb_list_databases Returns list of all databases in MongoDB

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :rtype: List All the databases in mongodb.
    """
    # Lets make sure the handle that is returned is not stale
    # and can connect to the MongoDB server
    try:
        handle.server_info()
    except (AutoReconnect, ServerSelectionTimeoutError) as e:
        print("[UNSKRIPT]: Reconnection / Server Selection Timeout Error: ", str(e))
        raise e
    except Exception as e:
        print("[UNSKRIPT]: Error Connecting: ", str(e))
        raise e

    dblist = handle.list_database_names()
    return dblist
