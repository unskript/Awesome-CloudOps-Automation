##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from typing import List, Any
from pydantic import BaseModel, Field
import psycopg2
from tabulate import tabulate


class InputSchema(BaseModel):
    function_name: str = Field(
        title='Function Name',
        description='Calling a PostgreSQL function')
    params: list = Field(
        None,
        title='Parameters',
        description='Parameters to the function in list format. For eg: [1, 2]')


def postgresql_call_function_printer(output):
    print("\n")
    if len(output) > 0:
        print("\n")
        print(tabulate(output, tablefmt="grid"))
    return output



def postgresql_call_function(handle, function_name: str, params: List = List[Any]) -> List:
    """postgresql_call_function Runs postgresql function with the provided parameters.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type function_name: str
        :param function_name: Function Name.

        :type params: List
        :param params: Parameters to the Function in list format.

        :rtype: List result of the function.
    """
    data = []
    try:
        cur = handle.cursor()
        cur.callproc(function_name, params)
        # process the result set
        res = cur.fetchall()

        for records in res:
            data.append(record for record in records)
        # Close communication with the PostgreSQL database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error : {error}")
    finally:
        if handle:
            handle.close()
    return data
