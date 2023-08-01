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
        indices_output = []
        # If no specific index is provided, get all indices
        if len(index_name)==0 :
            indices_output = handle.web_request("/_cat/indices?h=index", "GET", None)
            indices_output = ''.join(indices_output).split('\n')
        # If a specific index is provided, only consider that index
        else:
            indices_output.append(index_name)

        all_indices_stats = []

        for current_index in indices_output:
            # Skip system indices
            if current_index.startswith('.'):
                continue
            index_stats = {}

            # Get settings for the current index
            settings_output = handle.web_request(f"/{current_index}/_settings", "GET", None)
            if "error" in settings_output:
                print(f"Error for settings of {current_index}")
                continue

            # Get stats for the current index
            stats_output = handle.web_request(f"/{current_index}/_stats", "GET", None)
            if "error" in stats_output:
                print(f"Error for stats of {current_index}")
                continue

            # Get any tasks associated with the current index
            tasks_output = handle.web_request(f"/_tasks?actions=*{current_index}*&detailed", "GET", None)

            # Get health of the current index
            health_output = handle.web_request(f"/_cat/indices/{current_index}?format=json", "GET", None)
            if "error" in health_output:
                print(f"Error for health of {current_index}")
                continue

            if settings_output:
                settings = settings_output.get(current_index, {}).get('settings', {}).get('index', {})
            else:
                settings = {}
            # Consolidate stats for the current index
            if health_output[0]['health'] in ['yellow', 'red']:
                index_stats = {
                    **health_output[0],
                    'settings': settings,
                    'stats': stats_output['_all']['total'],
                    'tasks': tasks_output['nodes']
                }
                all_indices_stats.append(index_stats)
    except Exception as e:
        raise e
    if len(all_indices_stats)!=0:
        return (False, all_indices_stats)
    return (True, None)
