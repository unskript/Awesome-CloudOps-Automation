##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List, Any


class InputSchema(BaseModel):
    query: str = Field(
        title='Write Query',
        description='Query to insert/update')
    params: List = Field(
        None,
        title='Parameters',
        description='Parameters to the query in list format. For eg: [1, 2, "abc"]')


def mssql_write_query(handle, query: str, params: List = List[Any]) -> None:
    """mssql_write_query Runs mssql query with the provided parameters.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :type query: str
          :param query: MSSQL insert/update query.

          :type params: List
          :param params: Parameters to the query in list format.

          :rtype: None if success. Exception on error.
      """
    cur = handle.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    handle.commit()
    cur.close()
    handle.close()
    return
