##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Any
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    query: str = Field(
        title='Write Query',
        description='MySQL insert/update query.')
    params: List = Field(
        None,
        title='Parameters',
        description='Parameters to the query in list format. For eg: [1, 2, "abc"]')


def mysql_write_query(handle, query: str, params: List = List[Any]) -> None:
    """mysql_write_query Runs mysql query with the provided parameters.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :type query: str
          :param query: MySQL insert/update query.

          :type params: List
          :param params: Parameters to the query in list format.

          :rtype: None if success. Exception on error.
      """
    # Input param validation.

    cur = handle.cursor()
    cur.execute(query, params)
    handle.commit()
    cur.close()
    handle.close()
