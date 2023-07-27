##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from typing import List
from tabulate import tabulate
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def postgresql_get_service_status_printer(output):
    """postgresql_service_status_printer prints the status of postgresql service.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :rtype: List of dictionaries for database, username and its status.

    """
    data = []
    for record in output:
        data.append(record)

    headers = ['Database Name', 'User Name', 'Status']
    try:
        print(tabulate(data, headers=headers, tablefmt="grid"))
    except Exception as e:
        raise e


def postgresql_get_service_status(handle) -> List:
    """postgresql_get_service_status connects to the postgresql and checks the service status.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :rtype: The status of the service.
    """
    # SQL query to check the postgresql service status.
    query = """
                SELECT 
                    pg_stat_activity.datname AS dbname, 
                    pg_stat_activity.usename AS username, 
                    pg_stat_activity.state 
                FROM 
                    pg_stat_activity;
            """
    try:
        cur = handle.cursor()
        cur.execute(query)
        res = cur.fetchall()

        # Filter out records with None values
        res = [record for record in res if all(item is not None for item in record)]

        handle.commit()
        cur.close()
        handle.close()
        return res
    except Exception as e:
        raise e


