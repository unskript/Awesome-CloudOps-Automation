##
##  Copyright (c) 2022 unSkript, Inc
##  All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from typing import Dict
from tabulate import tabulate
from mongodb.legos.mongodb_util import reachable

from beartype import beartype

class InputSchema(BaseModel):
    query_secs_running_threshold: int = Field(
        default = 5,
        title = "Query Duration",
        description = "Query Duration in seconds. Eg. 5 or 10"
    )

def mongodb_list_long_running_queries_printer(output):
    if output is None:
        return
    if len(output.get('inprog')) == 0:
        print("No Long Queries detected") 
        return
    results = [['appName', 'active', 'op', 'ns', 'secs_running', 'desc']]
    try:
        for idx,query in enumerate(output.get('inprog')):
                result = []
                if 'appName' in query.keys():
                    result.append(query.get('appName'))
                else:
                    result.append('None')
                result.append(query.get('active'))
                result.append(query.get('op'))
                result.append(query.get('ns'))
                result.append(query.get('secs_running'))
                result.append(query.get('desc'))
                results.append(result)
    except Exception as e:
        print(f"Exception occured {e}")

    print(tabulate(results, headers="firstrow"))


@beartype
def mongodb_list_long_running_queries(handle, query_secs_running_threshold=5) -> Dict:
    """mongodb_list_long_running_queries  returns information on all the long running queries.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :rtype: Result of the query in the Dictionary form.
    """
    # Check the MongoDB 
    try: 
        reachable(handle)
    except Exception as e:
        raise e

    try:
        resp = handle.admin.command("currentOp", {"secs_running": {"$gt": query_secs_running_threshold}})
        return resp
    except Exception as e:
        raise e