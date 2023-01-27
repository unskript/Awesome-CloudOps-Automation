##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import random
import string
from typing import Any, List

from pydantic import BaseModel, Field
from tabulate import tabulate


class InputSchema(BaseModel):
    query: str = Field(
        title='Read Query',
        description='''
            Read query in Postgresql PREPARE statement format. For eg.
            SELECT foo FROM table WHERE bar=%s AND customer=%s.
            The values for %s and %s should be passed in the params field as a tuple.
        ''')
    params: tuple = Field(
        None,
        title='Parameters',
        description='Parameters to the query in tuple format. For eg: ("abc")')


def postgresql_read_query_printer(output):
    print("\n")
    data = []
    for records in output:
        data.append(record for record in records)
    print(tabulate(data, tablefmt="grid"))
    return output


def postgresql_read_query(handle, query: str, params: tuple = ()) -> List:
    """postgresql_read_query Runs postgresql query with the provided parameters.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :type query: str
          :param query: Postgresql read query.

          :type params: tuples
          :param params: Parameters to the query in tuple format.

          :rtype: List of Result of the Query.
      """

    cur = handle.cursor()
    # cur.execute(query, params)

    random_id = ''.join(
        [random.choice(string.ascii_letters + string.digits) for n in range(32)])

    query = "PREPARE psycop_{random_id} AS {query};".format(
        random_id=random_id, query=query)
    prepared_query = "EXECUTE psycop_{random_id};".format(
        random_id=random_id)
    cur.execute(query, params)
    cur.execute(prepared_query, params)
    res = cur.fetchall()
    handle.commit()
    cur.close()
    handle.close()
    return res
