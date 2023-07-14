##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import random
import string
from typing import List
from pydantic import BaseModel, Field
from tabulate import tabulate


class InputSchema(BaseModel):
    query: str = Field(
        title='Read Query',
        description='''
            Read query in Postgresql PREPARE statement format. For eg.
            SELECT foo FROM table WHERE bar=$1 AND customer=$2.
            The values for $1 and $2 should be passed in the params field as a tuple.
        ''')
    params: List = Field(
        None,
        title='Parameters',
        description='Parameters to the query in list format. For eg: [1, 2, "abc"]')


def postgresql_read_query_printer(output):
    print("\n")
    data = []
    for records in output:
        data.append(record for record in records)
    print(tabulate(data, tablefmt="grid"))
    return output


def postgresql_read_query(handle, query: str, params: list = ()) -> List:
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

    query = f"PREPARE psycop_{random_id} AS {query};"
    if not params:
        prepared_query = f"EXECUTE psycop_{random_id};"
    else:
        parameters_tuple = tuple(params)
        ## If there is only one tuple element, remove the trailing comma before format
        if len(parameters_tuple) == 1:
            tuple_string = str(parameters_tuple)
            parameters_tuple = tuple_string[:-2] + tuple_string[-1]
        prepared_query = f"EXECUTE psycop_{random_id} {params};"
    cur.execute(query)
    cur.execute(prepared_query)
    res = cur.fetchall()
    cur.close()
    return res
