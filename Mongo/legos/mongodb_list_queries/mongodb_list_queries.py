##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from pydantic import BaseModel
from typing import Dict

class InputSchema(BaseModel):
    pass

def mongodb_list_queries_printer(output):
    if output is None:
        return
    print("\n\n")
    if isinstance(output, Exception):
        pprint.pprint("Error : {}".format(output))
    else:
        pprint.pprint(output['inprog'])


def mongodb_list_queries(handle) -> Dict:
    """mongodb_list_queries can returns information on all the operations running.

        :type handle: object
        :param handle: Object returned from task.validate(...).


        :rtype: Dict All the results of the query.
    """
    try:
        resp = handle.admin.command(({"currentOp": True}))
        return resp
    except Exception as e:
        return {"Error": e}
