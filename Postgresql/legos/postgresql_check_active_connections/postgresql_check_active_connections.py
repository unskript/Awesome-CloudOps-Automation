##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from tabulate import tabulate


class InputSchema(BaseModel):
    threshold_connections: Optional[int] = Field(
        100,
        description='Number of connections to consider as the threshold.',
        title='Threshold no. of connections',
    )


def postgresql_check_active_connections_printer(output):
    status, data = output

    if not status and data:
        headers = ["Active Connections", "Threshold(%)"]
        table_data = [[record["active_connections"], record["threshold"]] for record in data]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print("Active connections are below the threshold.")


def postgresql_check_active_connections(handle, threshold_percentage: int = 85) -> Tuple:
    """
    postgresql_check_active_connections checks if the percentage of active connections to the database 
    exceeds the provided threshold.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :type threshold_percentage: float
    :param threshold_percentage: Optional, percentage of connections to consider as the threshold.

    :rtype: Status, Result of active connections if any in tabular format
    """
    # Query to fetch the count of active connections
    query_active_connections = "SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'active';"
    # Query to fetch the total pool count
    query_pool_count = "SELECT setting::int FROM pg_settings WHERE name='max_connections';"

    result = []
    try:
        cur = handle.cursor()

        # Fetch the total pool count
        cur.execute(query_pool_count)
        total_pool_count = cur.fetchone()[0]
        print(total_pool_count)

        # Calculate the threshold from the total pool count
        threshold = int((total_pool_count * threshold_percentage)/100)

        # Fetch the count of active connections
        cur.execute(query_active_connections)
        active_connections = cur.fetchone()[0]

        handle.commit()
        cur.close()
        handle.close()

        if active_connections > threshold:
            data = {
                "active_connections": active_connections,
                "threshold": threshold,
            }
            result.append(data)

    except Exception as e:
        print("Error occurred:", e)

    if len(result) != 0:
        return (False, result)
    return (True, None)

