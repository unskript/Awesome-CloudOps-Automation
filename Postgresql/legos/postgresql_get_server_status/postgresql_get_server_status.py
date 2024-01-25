##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from typing import Tuple, Optional
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    connection_threshold: Optional[int] = Field(
        10000,
        title='Connection threshold',
        description='Threshold for the number of connections considered abnormal. Default- 10000 clients')
    cache_hit_ratio_threshold: Optional[int] = Field(
        90,
        title='Cache hit ratio threshold (in %)',
        description='Threshold for the cache hit ratio considered abnormal. Default- 90%')
    blocked_query_threshold: Optional[int] = Field(
        10000,
        title='Blocked query threshold',
        description='TThreshold for the number of blocked queries considered abnormal. Default- 10000')


def postgresql_get_server_status_printer(output):
    is_healthy, server_status_info = output

    print("PostgreSQL Server Status:")
    print(f"  Overall Health: {'Healthy' if is_healthy else 'Unhealthy'}")
    print(f"  Total Connections: {server_status_info['total_connections']}")
    print(f"  Cache Hit Ratio: {server_status_info['cache_hit_ratio']}%")
    print(f"  Blocked Queries: {server_status_info['blocked_queries']}")

    abnormal_metrics = server_status_info.get('abnormal_metrics')
    if abnormal_metrics:
        print("\nAbnormal Metrics:")
        for metric in abnormal_metrics:
            print(f"  - {metric}")

def postgresql_get_server_status(handle, connection_threshold: int = 10000, cache_hit_ratio_threshold: int = 90, blocked_query_threshold: int = 10000) -> Tuple:
    """
    Returns the status of the PostgreSQL instance.

    :type handle: object
    :param handle: PostgreSQL connection object

    :type handle: object
    :param connection_threshold: Threshold for the number of connections considered abnormal

    :type handle: object
    :param cache_hit_ratio_threshold: Threshold for the cache hit ratio considered abnormal

    :type handle: object
    :param blocked_query_threshold: Threshold for the number of blocked queries considered abnormal

    :return: Tuple containing a status and a dictionary with detailed information
    """
    server_status_info = {}
    abnormal_metrics = []

    try:
        cur = handle.cursor()

        # Check total number of connections
        cur.execute("SELECT COUNT(*) FROM pg_stat_activity;")
        total_connections = cur.fetchone()[0]
        server_status_info['total_connections'] = total_connections
        if total_connections > connection_threshold:
            abnormal_metrics.append(f"High number of connections: {total_connections}")

        # Check cache hit ratio
        cur.execute("SELECT sum(heap_blks_hit) / sum(heap_blks_hit + heap_blks_read) * 100 AS ratio FROM pg_statio_user_tables;")
        cache_hit_ratio = cur.fetchone()[0]
        server_status_info['cache_hit_ratio'] = cache_hit_ratio
        if cache_hit_ratio < cache_hit_ratio_threshold:
            abnormal_metrics.append(f"Cache hit ratio below {cache_hit_ratio_threshold}%: {cache_hit_ratio}")

        # Check blocked queries
        cur.execute("SELECT COUNT(*) FROM pg_locks WHERE granted = false;")
        blocked_queries = cur.fetchone()[0]
        server_status_info['blocked_queries'] = blocked_queries
        if blocked_queries > blocked_query_threshold:
            abnormal_metrics.append(f"Blocked queries above threshold: {blocked_queries}")

        # Append abnormal metrics if any are found
        if abnormal_metrics:
            server_status_info['abnormal_metrics'] = abnormal_metrics
            return (False, server_status_info)

        return (True, server_status_info)

    except Exception as e:
        raise e
    finally:
        handle.close()


