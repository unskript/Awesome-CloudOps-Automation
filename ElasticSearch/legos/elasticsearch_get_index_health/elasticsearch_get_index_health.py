##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Tuple, Optional


class InputSchema(BaseModel):
    index_name: Optional[str] = Field(
        '',
        description='Name of the index for which the health is checked. If no index is provided, the health of all indices is checked.',
        title='Index name',
    )


def elasticsearch_get_index_health_printer(result):
    success, outputs = result
    if success or outputs is None or len(outputs) == 0:
        print("No indices found with 'yellow' or 'red' health.")
        return
    for output in outputs:
        print(f"\nProcessing index: {output['index']}")
        print("--------------------------------------------------")
        print(f"Health: {output['health']}")
        print(f"Status: {output['status']}")
        print(f"Documents count: {output['docs.count']}")
        print(f"Documents deleted: {output['docs.deleted']}")
        print(f"Store size: {output['store.size']}")
        print(f"Primary shards: {output['pri']}")
        print(f"Replicas: {output['rep']}")
        print("\nKey Settings:")
        print(f"  number_of_shards: {output['settings'].get('number_of_shards')}")
        print(f"  number_of_replicas: {output['settings'].get('number_of_replicas')}")
        print("--------------------------------------------------")




def elasticsearch_get_index_health(handle, index_name="") -> Tuple:
    """
    elasticsearch_get_index_health checks the health of a given Elasticsearch index or all indices if no specific index is provided.

    :type handle: object
    :param handle: Object returned from Task Validate

    :type index_name: str
    :param index_name: Name of the index for which the health is checked. If no index is provided, the health of all indices is checked.

    :rtype: list
    :return: A list of dictionaries where each dictionary contains stats about each index
    """
    try:
        health_url = f"/_cat/indices/{index_name}?v&h=index,health&format=json" if index_name else "/_cat/indices?v&h=index,health&format=json"
        health_response = handle.web_request(health_url, "GET", None)
        if not health_response:
            print(f"No indices found or error retrieving indices: {health_response.get('error', 'No response') if health_response else 'No data'}")
            return (True, None)

        # Filter indices that are not 'green'
        problematic_indices = [
            {"index": idx['index'], "health": idx['health']}
            for idx in health_response if idx['health'] != 'green'
        ]

        if not problematic_indices:
            print("All indices are in good health.")
            return (True, None)

    except Exception as e:
        print(f"Error processing index health: {str(e)}")
        return (False, [])

    return (False, problematic_indices)

