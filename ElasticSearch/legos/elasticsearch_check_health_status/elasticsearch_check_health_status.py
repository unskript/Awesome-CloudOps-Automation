##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Tuple


class InputSchema(BaseModel):
    pass

def elasticsearch_check_health_status_printer(output):
    if output is None:
        return
    print(output)


def elasticsearch_check_health_status(handle) -> Tuple:
    """elasticsearch_check_health_status checks the status of an Elasticsearch cluster .

            :type handle: object
            :param handle: Object returned from Task Validate

            :rtype: Result Tuple of result
    """
    result = []
    cluster_health ={}
    output = handle.web_request("/_cluster/health?pretty", "GET", None)

    if output['status'] != 'green':
        cluster_health['cluster_name'] = output['cluster_name']
        cluster_health['status'] = output['status']

        # Check for unassigned shards
        if output['unassigned_shards'] > 0:
            cluster_health['unassigned_shards'] = output['unassigned_shards']

        # Check for delayed unassigned shards
        if output['delayed_unassigned_shards'] > 0:
            cluster_health['delayed_unassigned_shards'] = output['delayed_unassigned_shards']

        # Check for any initializing or relocating shards
        if output['initializing_shards'] > 0 or output['relocating_shards'] > 0:
            cluster_health['initializing_shards'] = output['initializing_shards']
            cluster_health['relocating_shards'] = output['relocating_shards']

        # Check for the number of nodes
        if output['number_of_nodes'] != output['number_of_data_nodes']:
            cluster_health['number_of_nodes'] = output['number_of_nodes']
            cluster_health['number_of_data_nodes'] = output['number_of_data_nodes']

        result.append(cluster_health)
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)