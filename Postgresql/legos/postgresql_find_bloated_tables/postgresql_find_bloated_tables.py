##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint

from typing import List, Any, Optional, Tuple
from tabulate import tabulate
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    max_percent_bloat: Optional[int] = Field(
        default=50,
        title='Maximum Percent Bloat',
        description='Upper threshold percentage value of table bloat. By default upper value is set to 50%.')
    min_percent_bloat: Optional[int] = Field(
        default=25,
        title='Minimum Percent Bloat',
        description='Lower threshold percentage value of table bloat. By default lower value is set to 25%.')
    max_size_bloat: Optional[int] = Field(
        default=50,
        title='Maximum Size Bloat (in MB)',
        description='Upper threshold size of table bloat in Megabytes. By default upper value is set to 1000 MB i.e. 1 GB.')
    min_size_bloat: Optional[int] = Field(
        default=25,
        title='Maximum Size Bloat (in MB)',
        description='Lower threshold size of table bloat in Megabytes. By default lower value is set to 20 MB.')


def postgresql_find_bloated_tables_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def postgresql_find_bloated_tables(handle, max_percent_bloat:int=50, min_percent_bloat:int=25,max_size_bloat:int=20, min_size_bloat:int= 1000) -> Tuple:
    """postgresql_find_bloated_tables returns bloated tables in a database
        
        NOTE- By default we filter for tables which are either 50%
                bloated and more than 20mb in size, or more than 25%
                bloated and more than 1GB in size

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :type max_percent_bloat: int
          :param max_percent_bloat: Optional, Upper threshold percentage value of table bloat. By default upper value is set to 50%.

          :type min_percent_bloat: int
          :param min_percent_bloatterval: Optional,  Lower threshold percentage value of table bloat. By default lower value is set to 25%.

          :type max_size_bloat: int
          :param max_size_bloat: Optional, Upper threshold size of table bloat in Megabytes. By default upper value is set to 1000 MB i.e. 1 GB.

          :type min_size_bloat: int
          :param min_size_bloat: Optional, Lower threshold size of table bloat in Megabytes. By default lower value is set to 20 MB.

          :rtype: Status, Bloated tables in a database
      """
    max_pct = int(max_percent_bloat)
    min_pct = int(min_percent_bloat)
    max_mb = int(max_size_bloat)
    min_mb = int(min_size_bloat)
    query = "WITH constants AS ( SELECT current_setting('block_size')::numeric AS bs, 23 AS hdr, 8 AS ma), "\
    "no_stats AS ( SELECT table_schema, table_name, n_live_tup::numeric as est_rows,pg_table_size(relid)::numeric as table_size "\
    "FROM information_schema.columns "\
    "JOIN pg_stat_user_tables as psut "\
    "ON table_schema = psut.schemaname "\
    "AND table_name = psut.relname "\
    "LEFT OUTER JOIN pg_stats "\
    "ON table_schema = pg_stats.schemaname "\
    "AND table_name = pg_stats.tablename "\
    "AND column_name = attname "\
    "WHERE attname IS NULL "\
    "AND table_schema NOT IN ('pg_catalog', 'information_schema') "\
    "GROUP BY table_schema, table_name, relid, n_live_tup "\
    "), "\
    "null_headers AS ( "\
    "SELECT "\
    "hdr+1+(sum(case when null_frac <> 0 THEN 1 else 0 END)/8) as nullhdr, "\
    "SUM((1-null_frac)*avg_width) as datawidth, "\
    "MAX(null_frac) as maxfracsum, "\
    "schemaname, "\
    "tablename, "\
    "hdr, ma, bs "\
    "FROM pg_stats CROSS JOIN constants "\
    "LEFT OUTER JOIN no_stats "\
    "ON schemaname = no_stats.table_schema "\
    "AND tablename = no_stats.table_name "\
    "WHERE schemaname NOT IN ('pg_catalog', 'information_schema') "\
    "AND no_stats.table_name IS NULL "\
    "AND EXISTS ( SELECT 1 "\
    "FROM information_schema.columns "\
    "WHERE schemaname = columns.table_schema "\
    "AND tablename = columns.table_name ) "\
    "GROUP BY schemaname, tablename, hdr, ma, bs "\
    "), "\
    "data_headers AS ( "\
    "SELECT "\
    "ma, bs, hdr, schemaname, tablename, "\
    "(datawidth+(hdr+ma-(case when hdr%ma=0 THEN ma ELSE hdr%ma END)))::numeric AS datahdr, "\
    "(maxfracsum*(nullhdr+ma-(case when nullhdr%ma=0 THEN ma ELSE nullhdr%ma END))) AS nullhdr2 "\
    "FROM null_headers "\
    "), "\
    "table_estimates AS ( "\
    "SELECT schemaname, tablename, bs, "\
    "reltuples::numeric as est_rows, relpages * bs as table_bytes, "\
    "CEIL((reltuples* "\
    "(datahdr + nullhdr2 + 4 + ma - "\
    "(CASE WHEN datahdr%ma=0 "\
    "THEN ma ELSE datahdr%ma END) "\
    ")/(bs-20))) * bs AS expected_bytes, "\
    "reltoastrelid "\
    "FROM data_headers "\
    "JOIN pg_class ON tablename = relname "\
    "JOIN pg_namespace ON relnamespace = pg_namespace.oid "\
    "AND schemaname = nspname "\
    "WHERE pg_class.relkind = 'r' "\
    "), "\
    "estimates_with_toast AS ( "\
    "SELECT schemaname, tablename, "\
    "TRUE as can_estimate, "\
    "est_rows, "\
    "table_bytes + ( coalesce(toast.relpages, 0) * bs ) as table_bytes, "\
    "expected_bytes + ( ceil( coalesce(toast.reltuples, 0) / 4 ) * bs ) as expected_bytes "\
    "FROM table_estimates LEFT OUTER JOIN pg_class as toast "\
    "ON table_estimates.reltoastrelid = toast.oid "\
    "AND toast.relkind = 't' "\
    "), "\
    "table_estimates_plus AS ( "\
    "SELECT current_database() as databasename, "\
    "schemaname, tablename, can_estimate, "\
    "est_rows, "\
    "CASE WHEN table_bytes > 0 "\
    "THEN table_bytes::NUMERIC "\
    "ELSE NULL::NUMERIC END "\
    "AS table_bytes, "\
    "CASE WHEN expected_bytes > 0 "\
    "THEN expected_bytes::NUMERIC "\
    "ELSE NULL::NUMERIC END "\
    "AS expected_bytes, "\
    "CASE WHEN expected_bytes > 0 AND table_bytes > 0 "\
    "AND expected_bytes <= table_bytes "\
    "THEN (table_bytes - expected_bytes)::NUMERIC "\
    "ELSE 0::NUMERIC END AS bloat_bytes "\
    "FROM estimates_with_toast "\
    "UNION ALL "\
    "SELECT current_database() as databasename, "\
    "table_schema, table_name, FALSE, "\
    "est_rows, table_size, "\
    "NULL::NUMERIC, NULL::NUMERIC "\
    "FROM no_stats "\
    "), "\
    "bloat_data AS ( "\
    "select current_database() as databasename, "\
    "schemaname, tablename, can_estimate, "\
    "table_bytes, round(table_bytes/(1024^2)::NUMERIC,3) as table_mb, "\
    "expected_bytes, round(expected_bytes/(1024^2)::NUMERIC,3) as expected_mb, "\
    "round(bloat_bytes*100/table_bytes) as pct_bloat, "\
    "round(bloat_bytes/(1024::NUMERIC^2),2) as mb_bloat, "\
    "table_bytes, expected_bytes, est_rows "\
    "FROM table_estimates_plus "\
    ") "\
    "SELECT databasename, schemaname, tablename, "\
    "can_estimate, "\
    "est_rows, "\
    "pct_bloat, mb_bloat, "\
    "table_mb "\
    "FROM bloat_data "\
    "WHERE ( pct_bloat >= "+str(max_pct)+" AND mb_bloat >= "+str(min_mb)+" ) "\
    "OR ( pct_bloat >= "+str(min_pct)+" AND mb_bloat >= "+str(max_mb)+" ) "\
    "ORDER BY pct_bloat DESC; "

    cur = handle.cursor()
    cur.execute(query)
    output = []
    res = cur.fetchall()
    data = []
    for records in res:
        result = {
            "database_name": records[0],
            "schema_name": records[1],
            "table_name": records[2],
            "can_estimate": records[3],
            "live_rows_count": records[4],
            "pct_bloat": records[5],
            "mb_bloat": records[6],
            "table_mb": records[7]
        }
        output.append(result)
        data.append([records[0], records[1], records[2], records[5], records[6]])

    if len(res) > 0:
        headers = ["db_name", "schema_name", "table_name", "pct_bloat", "mb_bloat"]
        output = tabulate(data, headers=headers, tablefmt="grid")

    handle.commit()
    cur.close()
    handle.close()
    if len(output) != 0:
        return (False, output)
    else:
        return (True, None)