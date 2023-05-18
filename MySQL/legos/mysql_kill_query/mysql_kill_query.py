##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    processId: int = Field(
        title='An processId',
        description='Kill the process based on processId'
    )

def mysql_kill_query_printer(output):
    if output is None:
        return
    print("\n\n")
    pprint.pprint(output)

def mysql_kill_query(handle, processId: int) -> str:
    """mysql_kill_query can kill queries (read process) that are running more or
    equal than given interval.

        :type handle: object
        :param handle: Object returned by task.validate(...).
        
        :type processId: int
        :param processId: Process ID as integer that needs to be killed

        :rtype: Result of the kill %d process for the given processId in a str form.
    """
    # Kill long running queries using processId
    try:
        query = "kill %d;" % processId
        cur = handle.cursor()
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        handle.close()
        return res
    except Exception as e:
        return {"Error": e}
