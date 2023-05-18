##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    op_id: int = Field(
        title='An operation ID',
        description='Kill the operation based on opid'
    )


def mongodb_kill_queries_printer(output):
    if output is None:
        return
    print("\n\n")
    pprint.pprint(output)



def mongodb_kill_queries(handle, op_id: int) -> Dict:
    """mongodb_kill_queries can kill queries (read operations) that
    are running on more than one shard in a cluster.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type database_name: str
        :param database_name: An operation ID.

        :rtype: All the results of the query.
    """
    # Input param validation.

    try:
        resp = handle.admin.command("killOp", op=op_id)
        return resp
    except Exception as e:
        return {"Error": e}
