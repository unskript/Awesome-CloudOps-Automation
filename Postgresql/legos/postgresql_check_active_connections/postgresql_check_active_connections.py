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
        headers = ["Active Connections"]
        table_data = [[record["active_connections"]] for record in data]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print("Active connections are below the threshold.")


def postgresql_check_active_connections(handle, threshold_connections: int = 100) -> Tuple:
    """
    postgresql_check_active_connections checks if the number of active connections to the database 
    exceeds the provided threshold.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :type threshold_connections: int
    :param threshold_connections: Optional, number of connections to consider as the threshold.

    :rtype: Status, Result of active connections if any in tabular format
    """
    # Query to fetch the count of active connections
    query = "SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'active';"

    result = []
    try:
        cur = handle.cursor()
        cur.execute(query)
        active_connections = cur.fetchone()[0]  # fetch the count from the result
        handle.commit()
        cur.close()
        handle.close()

        if active_connections > threshold_connections:
            data = {
                "active_connections": active_connections,
            }
            result.append(data)

    except Exception as e:
        print("Error occurred:", e)

    if len(result) != 0:
        return (False, result)
    return (True, None)

