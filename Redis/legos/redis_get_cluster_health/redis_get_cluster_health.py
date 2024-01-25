#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import Optional, Tuple
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    client_threshold: Optional[int] = Field(
        10000,
        title='Client threshold',
        description='Threshold for the number of connected clients considered abnormal. Default- 100 clients')
    memory_threshold: Optional[int] = Field(
        80,
        title='Memory threshold (in %)',
        description='Threshold for the percentage of memory usage considered abnormal. Default- 80%')



def redis_get_cluster_health_printer(output):
    if output is None or not output[1]:
        print("No health information available.")
        return

    status, analysis = output

    print("\nRedis Health Info:")
    if status:
        print("Status: Healthy")
    else:
        print("Status: Unhealthy")

    for key, value in analysis.items():
        if key != 'abnormal_metrics':
            print(f"{key}: {value}")

    if 'abnormal_metrics' in analysis:
        print("\nAbnormal Metrics Detected:")
        for metric, message in analysis['abnormal_metrics']:
            print(f"{metric}: {message}")


def redis_get_cluster_health(handle, client_threshold: int = 10000, memory_threshold: int = 80) -> Tuple:
    """Returns the health of the Redis instance.
    
    :type handle: object
    :param handle: Redis connection object
    
    :type client_threshold: int
    :param client_threshold: Threshold for the number of connected clients considered abnormal
    
    :type memory_threshold: int
    :param memory_threshold: Threshold for the percentage of memory usage considered abnormal
    
    :rtype: Tuple containing a boolean indicating overall health and a dictionary with detailed information
    """
    # Metrics that need to be checked
    health_metrics = [
        'uptime_in_seconds',
        'connected_clients',
        'used_memory',
        'maxmemory',
        'rdb_last_bgsave_status',
        'aof_last_bgrewrite_status',
        'aof_last_write_status',
    ]

    health_info = {}
    abnormal_metrics = []

    try:
        general_info = handle.info()
        if not isinstance(general_info, dict):
            raise Exception("Unexpected format for general info")

        # Iterate through the health metrics to check for soecific keys
        for key in health_metrics:
            value = general_info.get(key)
            if value is None:
                continue

            health_info[key] = value

            # Check if connected clients exceed the threshold
            if key == 'connected_clients' and int(value) > client_threshold:
                abnormal_metrics.append((key, f"High number of connected clients: {value}"))

            # Check if memory usage exceeds the threshold
            if key == 'used_memory' and general_info.get('maxmemory') and int(value) / int(general_info['maxmemory']) * 100 > memory_threshold:
                abnormal_metrics.append((key, f"Memory utilization is above {memory_threshold}%: {value}"))

            # Check for abnormal statuses
            if key in ['rdb_last_bgsave_status', 'aof_last_bgrewrite_status', 'aof_last_write_status'] and value != 'ok':
                abnormal_metrics.append((key, f"Status not OK: {value}"))


        # Append abnormal metrics if any are found
        if abnormal_metrics:
            health_info['abnormal_metrics'] = abnormal_metrics
            return (False, health_info)

        return (True, health_info)

    except Exception as e:
        raise e
