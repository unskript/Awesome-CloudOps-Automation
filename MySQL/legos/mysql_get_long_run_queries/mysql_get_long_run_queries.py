##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List
from pydantic import BaseModel, Field
from tabulate import tabulate


class InputSchema(BaseModel):
    interval: int = Field(
        default=5,
        title='Interval(in seconds)',
        description='Return queries running longer than this interval')


def mysql_read_query_printer(output):
    if output is None:
        return
    print('\n')
    print(tabulate(output))


def mysql_get_long_run_queries(handle, interval: int = 5) -> List:
    """mysql_get_long_run_queries Runs returns information on all the MySQL long running queries.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type interval: int
        :param interval: Integer value to filter queries which runs above interval time.

        :rtype: Result of the query in the List form.
      """
    # Get long running queries
    try:
        query = ("SELECT PROCESSLIST_ID, PROCESSLIST_INFO FROM performance_schema.threads "
                 f"WHERE PROCESSLIST_COMMAND = 'Query' AND PROCESSLIST_TIME >= {interval};")

        cur = handle.cursor()
        cur.execute(query)

        res = cur.fetchall()

        cur.close()
        handle.close()
        return res

    except Exception as e:
        return {"Error": e}
