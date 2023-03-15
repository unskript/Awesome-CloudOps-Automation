##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint 
from typing import List, Any, Optional, Tuple
from pydantic import BaseModel, Field


def postgresql_get_cache_hit_ratio_printer(output):
    if output is None:
        return
    
    if len(output) > 0:
        cache_hit_ratio = output[0][2] * 100
        print(f"Cache hit ratio: {cache_hit_ratio:.2f}%")
    else:
        print("No cache hit ratio data available.")


def postgresql_get_cache_hit_ratio(handle) -> List:
    """postgresql_get_cache_hit_ratio Runs postgresql query to get the Cache hit ratio.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :rtype: All the results of the query.
      """

    # Query to get the Cache hit ratio.
    query = """SELECT sum(heap_blks_read) as heap_read, sum(heap_blks_hit)  as heap_hit, 
            sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio FROM pg_statio_user_tables;"""

    cur = handle.cursor()
    cur.execute(query)
    res = cur.fetchall()
    handle.commit()
    cur.close()
    handle.close()
    return res