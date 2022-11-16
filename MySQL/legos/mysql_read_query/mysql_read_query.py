##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List,Any
from tabulate import tabulate
import pprint


class InputSchema(BaseModel):
    query: str = Field(
        title='Read Query',
        description='MySQL get query.')
    params: List = Field(
        None,
        title='Parameters',
        description='Parameters to the query in list format. For eg: [1, 2, "abc"]')


def mysql_read_query_printer(output):
    if output is None:
        return
    print('\n')
    pprint.pprint(tabulate(output))


def mysql_read_query(handle, query: str, params: List = List[Any]) -> List:
    """mysql_read_query Runs mysql query with the provided parameters.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :type query: str
          :param query: MySQL get query.

          :type params: List
          :param params: Parameters to the query in list format.

          :rtype: List of  the results of the query.
      """
    # Input param validation.

    cur = handle.cursor()
    cur.execute(query, params)

    res = cur.fetchall()

    cur.close()
    handle.close()
    return res
