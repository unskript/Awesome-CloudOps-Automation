#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Dict
from pydantic import BaseModel
from tabulate import tabulate


class InputSchema(BaseModel):
    pass



def redis_get_metrics_printer(output):
    if output is None:
        return
    print("\nRedis Metrics: ")
    headers = ["Metric", "Value"]
    data = list(output.items())
    print(tabulate(data, headers, tablefmt="pretty"))


def bytes_to_human_readable(bytes, units=[' bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']):
    # Return a human-readable string representation of bytes.
    return str(bytes) + units[0] if bytes < 1024 else bytes_to_human_readable(bytes >> 10, units[1:])


def redis_get_metrics(handle) -> Dict:
    """
    redis_get_metrics returns redis metrics like index size, memory utilization.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :rtype: Dict containing index size and memory usage metrics
    """
    metrics = {}
    try:
        # Getting the information about redis server
        info = handle.info()

        # Initialize keys counter
        total_keys = 0

        # Iterate over all dbs in the info output
        for key in info:
            if key.startswith('db'):
                total_keys += info[key]['keys']
        metrics['index_size'] = total_keys #Total number of keys.
        metrics['memory_utilization'] = bytes_to_human_readable(info['used_memory'])
        metrics['dataset_size'] = bytes_to_human_readable(info['used_memory_dataset'])

    except Exception as e:
        metrics["error"] = str(e)
    return metrics



