##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Tuple
from pydantic import BaseModel
from tabulate import tabulate


class InputSchema(BaseModel):
    pass



def mongodb_get_metrics_printer(output):
    if not output:
        return
    total_memory, index_outputs = output
    if total_memory:
        print(f"Total Memory: {total_memory[0].get('Memory (MB)')} MB")

    print(tabulate(index_outputs, headers="keys"))


def mongodb_get_metrics(handle) -> Tuple:
    """
    mongodb_get_metrics retrieves various metrics such as index size,
    disk size per collection for all databases and collections.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :rtype: list of dictionaries with index size, storage size metrics and total memory usage in MB
    
    """
    index_metrics = []
    database_metrics = []
    try:
        database_names = handle.list_database_names()

        server_status = handle.admin.command("serverStatus")
        total_memory_MB = server_status['mem']['resident']  # Get the total resident set size in memory

        database_metrics.append({
            'Database': 'ALL',
            'Collection': 'ALL',
            'Memory (MB)': total_memory_MB,
        })

        for db_name in database_names:
            db = handle[db_name]
            collection_names = [coll['name'] for coll in db.list_collections() if not coll['options'].get('viewOn')]
            for coll_name in collection_names:
                stats = db.command("collstats", coll_name)

                index_size_KB = sum(stats.get('indexSizes', {}).values())/ 1024 # Convert bytes to KB
                storage_size_KB = stats.get('storageSize', 0)/ 1024 # Convert bytes to KB

                index_metrics.append({
                    'Database': db_name,
                    'Collection': coll_name,
                    'Index Size (KB)': index_size_KB,
                    'Storage Size (KB)': storage_size_KB,
                })

    except Exception as e:
        raise e
    return database_metrics, index_metrics