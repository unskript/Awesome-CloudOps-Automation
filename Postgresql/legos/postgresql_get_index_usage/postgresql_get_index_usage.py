##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint 
from typing import List, Any, Optional, Tuple
from tabulate import tabulate
from pydantic import BaseModel, Field


def postgresql_get_index_usage_printer(output):
    data = []
    for records in output:
        data.append(record for record in records)
    headers = ['Table Name', 'Index Usage Percentage', 'Number of Rows']
    print(tabulate(data, headers=headers, tablefmt="grid"))


def postgresql_get_index_usage(handle) -> List:
    """postgresql_get_index_usage Runs postgresql query to get index usage.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :rtype: All the results of the query.
      """
    # Query to get the Index Usage.
    query = """
                SELECT
                  relname,
                  100 * idx_scan / (seq_scan + idx_scan) percent_of_times_index_used,
                  n_live_tup rows_in_table
                FROM
                  pg_stat_user_tables
                WHERE
                    seq_scan + idx_scan > 0
                ORDER BY
                  n_live_tup DESC;
            """

    cur = handle.cursor()
    cur.execute(query)
    res = cur.fetchall()
    handle.commit()
    cur.close()
    handle.close()
    return res