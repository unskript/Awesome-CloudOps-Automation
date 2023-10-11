##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import List
from pydantic import BaseModel
from tabulate import tabulate


class InputSchema(BaseModel):
    pass


def mongodb_get_replica_set_printer(output):
    if output is None:
        print("No data found")
        return
    headers = ["Replica Name", "Role"]
    table = [(o['name'], o['role']) for o in output]
    print(tabulate(table, headers=headers, tablefmt='grid'))


def mongodb_get_replica_set(handle) -> List:
    """
    mongodb_get_replica_set retrieves the primary replica and a list of secondary replicas from a MongoDB replica set.

    :type handle: object
    :param handle: Object of type unskript connector to connect to MongoDB client

    :return: A list of dictionaries where each dictionary contains the name of the replica and its role.
    """
    replica_status = handle.admin.command("replSetGetStatus")
    replicas = []

    for member in replica_status['members']:
        role = member['stateStr'] 
        replicas.append({
            'name': member['name'],
            'role': role
        })

    return replicas



