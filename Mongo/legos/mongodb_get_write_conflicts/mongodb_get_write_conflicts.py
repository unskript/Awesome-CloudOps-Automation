##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Dict
from pydantic import BaseModel



class InputSchema(BaseModel):
    pass


def mongodb_get_write_conflicts_printer(output):
    if output is None:
        return
    print("Potential Write Conflicts:", output.get("totalWriteConflicts", "N/A"))


def mongodb_get_write_conflicts(handle) -> Dict:
    """
    mongodb_get_write_conflicts Retrieves potential write conflict metrics from the serverStatus command.

    :type handle: object
    :param handle: Object of type unskript connector to connect to MongoDB client

    :return: A dictionary containing metrics related to potential write conflicts.
    """

    server_status = handle.admin.command("serverStatus")

    write_conflict_metrics = {
        "totalWriteConflicts": server_status.get("wiredTiger", {}).get("concurrentTransactions", {}).get("write", {}).get("out", 0)
    }

    return write_conflict_metrics



