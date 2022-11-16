##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Tuple
from tabulate import tabulate
from typing import List



class InputSchema(BaseModel):
    query: str = Field(
        title='Read Query',
        description='Read query eg: select * from test;')
    params: Tuple = Field(
        None,
        title='Parameters',
        description='Parameters to the query in list format. For eg: [1, 2, "abc"]')


def mssql_read_query_printer(output):
    if output is None:
        return
    print('\n')
    print(tabulate(output))


def mssql_read_query(handle, query: str, params: Tuple = ()) -> List:
    """mssql_read_query Runs mssql query with the provided parameters.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :type query: str
          :param query: MSSQL read query.

          :type params: Tuple
          :param params: Parameters to the query in Tuple format.

          :rtype: List result of the query.
      """
    cur = handle.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)

    res = cur.fetchall()

    cur.close()
    handle.close()
    return res
