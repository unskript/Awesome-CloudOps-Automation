##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Tuple, Optional


class InputSchema(BaseModel):
    unassigned_shards: Optional[int] = Field(
        20,
        description='Threshold number of unassigned shards. Default - 20',
        title='Number of unassigned shards'
    )

def elasticsearch_check_health_status_printer(output):
    if output is None:
        return
    print(output)


def elasticsearch_check_health_status(handle, unassigned_shards:int = 20) -> Tuple:
    """elasticsearch_check_health_status checks the status of an Elasticsearch cluster .

            :type handle: object
            :param handle: Object returned from Task Validate

            :rtype: Result Tuple of result
    """
    output = handle.web_request("/_cluster/health?pretty", "GET", None)
    
    # Early return if cluster status is green
    if output['status'] == 'green':
        return (True, None)
    
    cluster_health = {
        "cluster_name": output['cluster_name'],
        "status": output['status'],
        "unassigned_shards": output['unassigned_shards']
    }
    
    # Check for significant health issues
    if output['unassigned_shards'] > unassigned_shards:
        return (False, [cluster_health])  # Return immediately if unassigned shards exceed the threshold

    # Additional checks for severe conditions
    if output['status'] == 'red' or output['delayed_unassigned_shards'] > 0 or output['initializing_shards'] > 0 or output['relocating_shards'] > 0 or output['number_of_nodes'] != output['number_of_data_nodes']:
        additional_details = {
            "delayed_unassigned_shards": output['delayed_unassigned_shards'],
            "initializing_shards": output['initializing_shards'],
            "relocating_shards": output['relocating_shards'],
            "number_of_nodes": output['number_of_nodes'],
            "number_of_data_nodes": output['number_of_data_nodes']
        }
        cluster_health.update(additional_details)
        return (False, [cluster_health])
    
    # If status is yellow but no additional critical issues, consider it healthy
    return (True, None)