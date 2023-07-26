#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Dict
from pydantic import BaseModel
from tabulate import tabulate


class InputSchema(BaseModel):
    pass



def redis_get_cluster_health_printer(output):
    if output is None:
        return
    print("\nRedis Cluster Health: ")
    headers = ["Metric", "Value"]
    data = list(output.items())
    print(tabulate(data, headers, tablefmt="pretty"))


def redis_get_cluster_health(handle) -> Dict:
    """
    redis_get_cluster_health returns the health of the Redis cluster.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :rtype: Dict containing cluster health information
    """
    health_info = {}
    try:
        # Get cluster info
        cluster_info = handle.execute_command("CLUSTER INFO")

        # Process the result
        for line in cluster_info.splitlines():
            key, value = line.split(':')
            health_info[key] = value

    except Exception as e:
        health_info["error"] = str(e)

    return health_info


