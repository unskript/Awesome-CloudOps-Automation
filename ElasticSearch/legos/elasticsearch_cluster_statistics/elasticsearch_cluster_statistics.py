##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List, Dict
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from tabulate import tabulate


class InputSchema(BaseModel):
    pass


def elasticsearch_cluster_statistics_printer(output):
    if output is None:
        return
    timestamp = datetime.fromtimestamp(output.get('timestamp')/1000)  # converting milliseconds to seconds
    print("\nCluster Name: ", output.get('cluster_name'))
    print("Timestamp: ", timestamp)
    print("Status: ", output.get('status'))

    # Node Statistics
    print("\nNode Statistics")
    nodes = output.get('_nodes')
    if nodes is not None:
        df = pd.DataFrame.from_records([nodes])
        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    else:
        print("Nodes are None")

    # Document Statistics
    print("\nDocument Statistics")
    df = pd.DataFrame.from_records([output.get('indices').get('docs')])
    df.columns = [f'{i} (count)' for i in df.columns]
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    # Shard Statistics
    print("\nShard Statistics")
    df = pd.DataFrame.from_records([output.get('indices').get('shards').get('index')])
    df.columns = [f'{i} (shard count)' for i in df.columns]
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    # Additional Metrics
    print("\nAdditional Metrics")
    additional_metrics = {
        'total_index_size (MB)': output.get('total_index_size'),
        'total_disk_size (MB)': output.get('total_disk_size'),
        'total_memory_utilization (%)': output.get('total_memory_utilization'),
    }
    df = pd.DataFrame.from_records([additional_metrics])
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))


def elasticsearch_cluster_statistics(handle) -> Dict:
    """elasticsearch_cluster_statistics fetches total index size, disk size, and memory utilization 
    and information about the current nodes and shards that form the cluster

            :type handle: object
            :param handle: Object returned from Task Validate

            :rtype: Result Dict of result
    """
    try:
        # Fetching cluster statistics
        output = handle.web_request("/_cluster/stats?human&pretty", "GET", None)

        # Fetching indices statistics
        indices_stats = handle.web_request("/_cat/indices?format=json", "GET", None)

        # Fetching nodes statistics
        nodes_stats = handle.web_request("/_nodes/stats?human&pretty", "GET", None)

        total_index_size = 0
        for index in indices_stats:
            size = index['store.size']
            if 'kb' in size:
                total_index_size += float(size.replace('kb', '')) / 1024
            elif 'mb' in size:
                total_index_size += float(size.replace('mb', ''))
            elif 'gb' in size:
                total_index_size += float(size.replace('gb', '')) * 1024

        total_disk_size = sum([float(node['fs']['total']['total_in_bytes']) for node in nodes_stats['nodes'].values()])
        total_disk_size /= (1024 * 1024)  # convert from bytes to MB

        total_memory = sum([float(node['jvm']['mem']['heap_used_percent']) for node in nodes_stats['nodes'].values()])

        # Adding additional metrics to the output
        output['total_index_size'] = total_index_size
        output['total_disk_size'] = total_disk_size
        output['total_memory_utilization'] = total_memory

    except Exception as e:
        raise e
    return output
