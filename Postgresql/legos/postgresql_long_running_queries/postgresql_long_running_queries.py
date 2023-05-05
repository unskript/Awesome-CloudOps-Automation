##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint 

from typing import List, Any, Optional, Tuple
from tabulate import tabulate
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    interval: Optional[int] = Field(
        default=5,
        title='Interval (in seconds)',
        description='Return queries running longer than interval')

def postgresql_long_running_queries_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def postgresql_long_running_queries(handle, interval: int = 5) -> Tuple:
    """postgresql_long_running_queries Runs postgres query with the provided parameters.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :type interval: int
          :param interval: Interval (in seconds).

          :rtype: All the results of the query.
      """
    # Input param validation.

    # Multi-line will create an issue when we package the Legos.
    # Hence concatinating it into a single line.
    query = "SELECT pid, user, pg_stat_activity.query_start, now() - " \
        "pg_stat_activity.query_start AS query_time, query, state " \
        " FROM pg_stat_activity WHERE state = 'active' AND " \
        "(now() - pg_stat_activity.query_start) > interval '%d seconds';" % interval


    cur = handle.cursor()
    cur.execute(query)
    output = []
    res = cur.fetchall()
    data = []
    for records in res:
        result = {
            "pid": records[0],
            "user": records[1],
            "query_start": records[2],
            "query_time": records[3],
            "query": records[4],
            "state": records[5]
        }
        output.append(result)
        data.append([records[0], records[4], records[5], records[3]])

    if len(res) > 0:
        headers = ["pid", "query", "state", "duration"]
        print("\n")
        output = tabulate(data, headers=headers, tablefmt="grid")

    handle.commit()
    cur.close()
    handle.close()
    if len(output) != 0:
        return (False, output)
    else:
        return (True, None)
