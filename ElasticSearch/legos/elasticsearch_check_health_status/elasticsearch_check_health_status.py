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
    cluster_health = {}
    output = handle.web_request("/_cluster/health?pretty", "GET", None)

    if output['status'] == 'green':
        return (True, None)

    cluster_health['cluster_name'] = output['cluster_name']
    cluster_health['status'] = output['status']

    # Additional checks for both red and yellow statuses
    additional_details = False
    if output['unassigned_shards'] > unassigned_shards:
        cluster_health['unassigned_shards'] = output['unassigned_shards']
        additional_details = True

    if output['delayed_unassigned_shards'] > 0:
        cluster_health['delayed_unassigned_shards'] = output['delayed_unassigned_shards']
        additional_details = True

    if output['initializing_shards'] > 0 or output['relocating_shards'] > 0:
        cluster_health['initializing_shards'] = output['initializing_shards']
        cluster_health['relocating_shards'] = output['relocating_shards']
        additional_details = True

    if output['number_of_nodes'] != output['number_of_data_nodes']:
        cluster_health['number_of_nodes'] = output['number_of_nodes']
        cluster_health['number_of_data_nodes'] = output['number_of_data_nodes']
        additional_details = True

    # If status is red, return the result immediately
    if output['status'] == 'red' or (output['status'] == 'yellow' and additional_details):
        return (False, [cluster_health])

    # If status is yellow but no additional conditions are met, return as healthy
    return (True, None)