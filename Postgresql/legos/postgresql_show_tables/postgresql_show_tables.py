##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from pydantic import BaseModel
from unskript.legos.postgresql.postgresql_read_query.postgresql_read_query import postgresql_read_query
from tabulate import tabulate
from typing import List


class InputSchema(BaseModel):
    pass

def postgresql_show_tables_printer(output):
    print("\n")
    data = []
    for records in output:
        data.append(record for record in records)
    print(tabulate(data, tablefmt="grid"))
    return output


def postgresql_show_tables(handle) -> List:
    """ppostgresql_show_tables gives list of tables.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :rtype: List of tables.
      """

    query = "SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"
    return postgresql_read_query(handle, query, ())
