##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Tuple, List, Any
import random
import string


class InputSchema(BaseModel):
    query: str = Field(
        title='Write Query',
        description='''
            INSERT/UPDATE query in Postgresql PREPARE statement format. For eg.
            INSERT INTO my_table VALUES($1, $2).
            The values for $1 and $2 should be passed in the params field as a list.
        ''')
    params: Tuple = Field(
        default=None,
        title='Parameters',
        description='Parameters to the query in list format. Eg [ 42, "abc" ]')


def postgresql_write_query(handle, query: str, params: List = List[Any]):
    """postgresql_write_query Runs postgresql query with the provided parameters.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :type query: str
          :param query: Postgresql insert/update query.

          :type params: List
          :param params: Parameters to the query in list format.

          :rtype: None if success. Exception on error.
      """

    cur = handle.cursor()

    random_id = ''.join(
        [random.choice(string.ascii_letters + string.digits) for n in range(32)])

    query = "PREPARE psycop_{random_id} AS {query};".format(
        random_id=random_id, query=query)
    if not params:
        prepared_query = "EXECUTE psycop_{random_id};".format(
            random_id=random_id)
    else:
        prepared_query = "EXECUTE psycop_{random_id} {params};".format(
            random_id=random_id, params=tuple(params))

    cur.execute(query)
    cur.execute(prepared_query)

    handle.commit()
    cur.close()
    handle.close()
    return
