##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from tabulate import tabulate


class InputSchema(BaseModel):
    connection_threshold: Optional[int] = Field(
        '1000',
        title='Connection threshold',
        description='Threshold for the number of connections considered abnormal. Default- 100 clients')
    memory_threshold: Optional[int] = Field(
        '2048',
        title='Memory threshold (in MB)',
        description='Threshold for the megabytes of resident memory usage considered abnormal (in megabytes). Default- 80%')
    cache_usage_threshold: Optional[int] = Field(
        '80',
        title='Cache usage threshold (in %)',
        description='Threshold for the percentage of WiredTiger cache usage considered abnormal. Default- 80%')



def mongodb_get_server_status_printer(output):
    if output is None or not output[1]:
        print("No MongoDB server status information available.")
        return

    status, analysis = output

    print("\nMongoDB Server Status:")
    if status:
        print("Status: Healthy")
    else:
        print("Status: Unhealthy")

    for key, value in analysis.items():
        if key == 'wiredTiger_cache':
            print("WiredTiger Cache:")
            for subkey, subvalue in value.items():
                print(f"  {subkey}: {subvalue}")
        elif key == 'replication_info':
            print("Replication Info:")
            for subkey, subvalue in value.items():
                print(f"  {subkey}: {subvalue}")
        elif key == 'locks':
            print("Locks:")
            for subkey, subvalue in value.items():
                print(f"  {subkey}: {subvalue}")
        else:
            print(f"{key}: {value}")



def mongodb_get_server_status(handle, connection_threshold: int = 100, memory_threshold: int = 2048, cache_usage_threshold: int = 80) -> Tuple:
    """Returns the status of the MongoDB instance.

    :type handle: object
    :param handle: MongoDB connection object

    :type connection_threshold: int
    :param connection_threshold: Threshold for the number of connections considered abnormal

    :type memory_threshold: int
    :param memory_threshold: Threshold for the megabytes of resident memory usage considered abnormal (in megabytes)

    :type cache_usage_threshold: int
    :param cache_usage_threshold: Threshold for the percentage of WiredTiger cache usage considered abnormal

    :return: Status indicating overall health and a dictionary with detailed information
    """
    server_status_info = {}
    abnormal_metrics = []
    
    try:
        server_status = handle.admin.command("serverStatus")

        # Essential metrics
        server_status_info['version'] = server_status['version']
        server_status_info['uptime'] = server_status['uptime']
        server_status_info['connections'] = server_status.get('connections', {}).get('current')
        server_status_info['resident_memory'] = server_status.get('mem', {}).get('resident')
        server_status_info['operation_counts'] = server_status['opcounters']
        server_status_info['asserts'] = server_status['asserts']
        server_status_info['wiredTiger_cache'] = server_status.get('wiredTiger', {}).get('cache')
        server_status_info['replication_info'] = server_status.get('repl')
        server_status_info['locks'] = server_status.get('locks')

        # Check if connections exceed the threshold
        if server_status_info['connections'] > connection_threshold:
            abnormal_metrics.append(f"High number of connections: {server_status_info['connections']}")

        # Check if resident memory usage exceeds the threshold (in megabytes)
        if server_status_info['resident_memory'] > memory_threshold:
            abnormal_metrics.append(f"Resident memory utilization is above {memory_threshold} MB: {server_status_info['resident_memory']}")

        # Check if WiredTiger cache usage exceeds the threshold
        wired_tiger_cache = server_status_info['wiredTiger_cache']
        if wired_tiger_cache:
            used_bytes = wired_tiger_cache.get('bytes currently in the cache')
            total_bytes = wired_tiger_cache.get('maximum bytes configured')
            if used_bytes is not None and total_bytes is not None:
                cache_usage = (used_bytes / total_bytes) * 100
                server_status_info['wiredTiger_cache_usage'] = cache_usage
                if cache_usage > cache_usage_threshold:
                    abnormal_metrics.append(f"Cache utilization is above {cache_usage_threshold}%")

        # Append abnormal metrics if any are found
        if abnormal_metrics:
            server_status_info['abnormal_metrics'] = abnormal_metrics
            return False, server_status_info

        return True, None

    except Exception as e:
        raise e
