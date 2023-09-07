##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from typing import Tuple
from pydantic import BaseModel
from tabulate import tabulate


class InputSchema(BaseModel):
    pass



def postgresql_check_locks_printer(output):
    status, data = output
    
    if not status and data:
        headers = ["PID", "Relation", "Lock Mode", "Granted"]
        table_data = [[record["pid"], record["relation"], record["lock_mode"], record["granted"]] for record in data]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print("No ungranted locks found.")


def postgresql_check_locks(handle) -> Tuple:
    """
    postgresql_check_locks identifies and returns the current locks in the PostgreSQL database.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :rtype: Status, Result of current locks if any in tabular format
    """
    # Query to fetch current locks in the database
    query = """
            SELECT 
                pid,
                relation::regclass,
                mode,
                granted
            FROM 
                pg_locks
            WHERE 
                granted IS FALSE;
            """

    result = []
    try:
        cur = handle.cursor()
        cur.execute(query)
        res = cur.fetchall()
        handle.commit()
        cur.close()
        handle.close()

        for record in res:
            data = {
                "pid": record[0],
                "relation": record[1],
                "lock_mode": record[2],
                "granted": record[3]
            }
            result.append(data)
    except Exception as e:
        print("Error occurred:", e)

    if len(result) != 0:
        return (False, result)
    return (True, None)

