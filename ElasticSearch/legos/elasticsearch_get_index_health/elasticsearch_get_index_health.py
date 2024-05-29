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
        if index_name:
            index_names = [index_name]
        else:
            # Fetches all indices; ensure only non-empty lines and non-system indices are considered
            response = handle.web_request("/_cat/indices?h=index", "GET", None)
            index_names = [line.strip() for line in response.splitlines() if line.strip() and not line.startswith('.')]

        all_indices_stats = []

        for current_index in index_names:
            health_url = f"/_cat/indices/{current_index}?format=json"
            health_response = handle.web_request(health_url, "GET", None)
            if not health_response or "error" in health_response:
                print(f"Error retrieving health for index {current_index}: {health_response.get('error', 'Unknown error')}")
                continue

            # Parsing the health data correctly assuming the correct format and keys are present
            health_data = health_response[0]
            if health_data.get('health') in ['yellow', 'red']:
                index_stats = {
                    "index": current_index,
                    "health": health_data.get('health'),
                    "status": health_data.get('status'),
                }
                all_indices_stats.append(index_stats)

    except Exception as e:
        print(f"Error processing index health: {str(e)}")
        return (False, [])

    return (False, all_indices_stats) if all_indices_stats else (True, None)

