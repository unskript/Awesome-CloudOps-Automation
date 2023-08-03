##  
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Tuple, Optional
from pydantic import BaseModel,Field


class InputSchema(BaseModel):
    threshold: Optional[float] = Field(
        1000, description='Threshold for index size in KB.', title='Threshold (in KB)'
    )



def elasticsearch_check_large_index_size_printer(result):
    success, alerts = result
    if success:
        print("Index sizes are within the threshold.")
        return
    for alert in alerts:
        print(f"Alert! Index size of {alert['indexSizeKB']} KB for index {alert['index']} exceeds threshold of {alert['threshold']} KB.")


def elasticsearch_check_large_index_size(handle, threshold: float = 1000) -> Tuple:
    """
    elasticsearch_check_large_index_size checks the sizes of all indices in the
    Elasticsearch cluster and compares them to a given threshold.

    :type handle: object
    :param handle: Object returned from Task Validate

    :type threshold: float
    :param threshold: The threshold for index size in KB.

    :return: Status, alerts (if any index size exceeds the threshold).
    """
    alerts = []

    try:
        # Request the list of all indices
        indices_output = handle.web_request("/_cat/indices?h=index", "GET", None)
        indices_output = ''.join(indices_output).split('\n')
        indices_output = [index for index in indices_output if index and not index.startswith('.')]

        for current_index in indices_output:
            # Request the stats for the current index
            stats_output = handle.web_request(f"/{current_index}/_stats", "GET", None)
            index_size_bytes = stats_output['_all']['total']['store']['size_in_bytes']
            index_size_KB = index_size_bytes / 1024

            # Check if the index size exceeds the threshold
            if index_size_KB > threshold:
                alerts.append({
                    'index': current_index,
                    'indexSizeKB': index_size_KB,
                    'threshold': threshold
                })

    except Exception as e:
        raise e

    if len(alerts) != 0:
        return (False, alerts)
    return (True, None)


