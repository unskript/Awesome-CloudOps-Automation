##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint

from typing import Optional, Tuple
from tabulate import tabulate
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    index_scans: Optional[int] = Field(
        default=50,
        title='Index Scans',
        description='Number of index scans initiated on this index')
    index_size: Optional[int] = Field(
        default=50000,
        title='Index Size',
        description='On-disk size in kB (kilobytes) of the table.')



def postgresql_check_unused_indexes_printer(output):
    if output is None:
        return
    data = []
    output_rows =[]
    for records in output:
        if type(records)==list:
            for r in records:
                result = {
                    "table": r[0],
                    "index": r[1],
                    "index_size": r[2],
                    "index_scans": r[3],
                }
                output_rows.append(result)
                data.append([r[0], r[1], r[2], r[3]])
            if len(output) > 0:
                headers = ["Table", "Index", "Index Size", "Index Scans"]
                output_rows = tabulate(data, headers=headers, tablefmt="grid")
    pprint.pprint(output_rows)


def postgresql_check_unused_indexes(handle, index_scans:int=50,index_size:int=50000) -> Tuple:
    """postgresql_check_unused_indexes returns unused indexes in a database

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :type index_scans: int
          :param index_scans: Optional, Number of index scans initiated on this index

          :type index_size: int
          :param index_size: Opitonal, On-disk size in kB (kilobytes) of the table.

          :rtype: Status, Result of unused indexes if any in tabular format
      """
    size = int(index_size)
    scans = int(index_scans)
    query = "SELECT schemaname || '.' || relname AS table,indexrelname AS index,pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size,idx_scan as index_scans " \
        " FROM pg_stat_user_indexes ui JOIN pg_index i ON ui.indexrelid = i.indexrelid "\
        " WHERE NOT indisunique AND idx_scan < " + str(scans) + " AND pg_relation_size(relid) > "+ str(size)+\
        " ORDER BY pg_relation_size(i.indexrelid) / nullif(idx_scan, 0) DESC NULLS FIRST,pg_relation_size(i.indexrelid) DESC "

    #In the above query:
    #pg_relation_size accepts the OID or name of a table, index or toast table, and returns the on-disk size in bytes of one fork of that relation. (Note that for most purposes it is more convenient to use the higher-level functions pg_total_relation_size or pg_table_size, which sum the sizes of all forks.) With one argument, it returns the size of the main data fork of the relation. The second argument can be provided to specify which fork to examine:
    # 1. 'main' returns the size of the main data fork of the relation.
    # 2. 'fsm' returns the size of the Free Space Map 
    # 3. 'vm' returns the size of the Visibility Map 
    # 4. 'init' returns the size of the initialization fork, if any, associated with the relation.
    # We are getting the main data fork size
    
    cur = handle.cursor()
    cur.execute(query)
    result = cur.fetchall()
    handle.commit()
    cur.close()
    handle.close()
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)
