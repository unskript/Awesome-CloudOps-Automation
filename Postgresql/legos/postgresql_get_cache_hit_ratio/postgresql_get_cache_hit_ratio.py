##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint 
from typing import Tuple
from pydantic import BaseModel

class InputSchema(BaseModel):
    pass

def postgresql_get_cache_hit_ratio_printer(output):
    if output is None or output[1] is None:
        print("No cache hit ratio data available.")
        return

    op = output[1]
    if len(op) > 0:
        cache_hit_ratio = op[0][2] * 100
        print(f"Cache hit ratio: {cache_hit_ratio:.2f}%")
    else:
        print("No cache hit ratio data available.")
        
    pprint.pprint(output)



def postgresql_get_cache_hit_ratio(handle) -> Tuple:
    """postgresql_get_cache_hit_ratio Runs postgresql query to get the Cache hit ratio.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :rtype: All the results of the query.
      """

    # Query to get the Cache hit ratio.
    query = """SELECT sum(heap_blks_read) as heap_read, sum(heap_blks_hit)  as heap_hit,
            sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio FROM 
            pg_statio_user_tables;"""

    cur = handle.cursor()
    cur.execute(query)
    res = cur.fetchall()
    handle.commit()
    cur.close()
    handle.close()

    if res is not None and len(res) > 0 and res[0][2] is not None:
        cache_hit_ratio = res[0][2] * 100
        if cache_hit_ratio >= 99:
            return (True, res)
        return (False, res)
    return (False, None)
