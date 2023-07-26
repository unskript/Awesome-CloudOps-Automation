##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import List
from pydantic import BaseModel
from tabulate import tabulate


class InputSchema(BaseModel):
    pass



def mongodb_get_metrics_printer(output):
    if not output:
        return

    total_memory_metric = next((metric for metric in output if metric['Database'] == 'ALL' and metric['Collection'] == 'ALL'), None)
    if total_memory_metric:
        print(f"Total Memory: {total_memory_metric['Memory (MB)']} MB")

    table_metrics = [metric for metric in output if 'Index Size (MB)' in metric]
    print(tabulate(table_metrics, headers="keys"))


def mongodb_get_metrics(handle) -> List:
    """
    mongodb_get_metrics retrieves various metrics such as index size,
    disk size per collection for all databases and collections.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :rtype: list of dictionaries with index size, storage size metrics and total memory usage in MB
    """
    all_metrics = []
    try:
        database_names = handle.list_database_names()

        server_status = handle.admin.command("serverStatus")
        total_memory_MB = server_status['mem']['resident']  # Get the total resident set size in memory

        all_metrics.append({
            'Database': 'ALL',
            'Collection': 'ALL',
            'Memory (MB)': total_memory_MB,
        })

        for db_name in database_names:
            db = handle[db_name]
            collection_names = db.list_collection_names()
            for coll_name in collection_names:
                stats = db.command("collstats", coll_name)

                index_size_MB = sum(stats.get('indexSizes', {}).values()) / 1024 / 1024 # Convert bytes to MB
                storage_size_MB = stats.get('storageSize', 0) / 1024 / 1024 # Convert bytes to MB

                all_metrics.append({
                    'Database': db_name,
                    'Collection': coll_name,
                    'Index Size (MB)': index_size_MB,
                    'Storage Size (MB)': storage_size_MB,
                })

    except Exception as e:
        raise e
    return all_metrics


