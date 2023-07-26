##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import List, Optional
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    index_threshold: Optional[float] = Field(
        10,
        description='The threshold for total index size. Default is 10MB.',
        title='Index threshold(in MB)',
    )
    memory_threshold: Optional[float] = Field(
        300,
        description='The threshold for memory utilization. Default is 300MB',
        title='Memory Threshold(in MB)',
    )



def mongodb_compare_index_size_and_memory_printer(output):
    if not output:
        print("Memory and index sizes are within their respective thresholds.")
        return

    for o in output:
        if o['type'] == 'index':
            print(f"Alert! Total index size of {o['totalIndexSizeMB']} MB for database {o['db']} exceeds threshold.")
        elif o['type'] == 'memory':
            print(f"Alert! Memory usage of {o['memoryMB']} MB exceeds threshold.")  # Removed database from the alert


def mongodb_compare_index_size_and_memory(handle, index_threshold:float=10, memory_threshold:float=300) -> List:
    """
    mongodb_compare_index_size_and_memory retrieves database metrics such as index size, 
    disk size per collection, and memory utilization for all databases. It calculates the total 
    index size and compares it with the index threshold, and also compares total memory 
    utilization with the memory threshold.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :type index_threshold: float
    :param index_threshold: The threshold for total index size

    :type memory_threshold: float
    :param memory_threshold: The threshold for memory utilization

    :rtype: A list of dictionaries. Each dictionary contains the name of a database that has exceeded 
             either index size or memory utilization thresholds and the size that was exceeded.
    """

    all_metrics = {}
    alerts = []

    try:
        database_names = handle.list_database_names()
        total_memory_MB = 0

        server_status = handle.admin.command("serverStatus")
        total_memory_MB += server_status['mem']['resident']  # Get the total resident set size in memory

        for db_name in database_names:
            db = handle[db_name]
            total_index_size_MB = 0  # Track the total index size for this database

            collection_names = db.list_collection_names()
            for coll_name in collection_names:
                stats = db.command("collstats", coll_name)
                index_size_MB = sum(stats['indexSizes'].values()) / 1024 / 1024
                total_index_size_MB += index_size_MB

            if total_index_size_MB > index_threshold:
                alerts.append({'db': db_name, 'totalIndexSizeMB': total_index_size_MB, 'type': 'index'})

            all_metrics[db_name] = {
                'totalIndexSize': total_index_size_MB,  # In MB
            }

        if total_memory_MB > memory_threshold:
            alerts.append({'memoryMB': total_memory_MB, 'type': 'memory'})

    except Exception as e:
        raise e
    return alerts



