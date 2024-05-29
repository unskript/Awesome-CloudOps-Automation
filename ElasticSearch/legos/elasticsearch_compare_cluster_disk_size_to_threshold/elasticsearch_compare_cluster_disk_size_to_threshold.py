##  
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Optional, Tuple
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    threshold: Optional[float] = Field(
        80, description='Threshold for disk usage percentage.', title='Threshold (in %)'
    )


def elasticsearch_compare_cluster_disk_size_to_threshold_printer(output):
    success, data = output
    if success:
        print("Cluster disk usage is within the threshold.")
    else:
        for item in data:
            print(f"Alert! Cluster disk usage of {item['usage_disk_percentage']}% exceeds the threshold of {item['threshold']}%.")

def elasticsearch_compare_cluster_disk_size_to_threshold(handle, threshold: float=80.0) -> Tuple:
    """
    elasticsearch_compare_cluster_disk_size_to_threshold compares the disk usage percentage of the Elasticsearch cluster to a given threshold.

    :type handle: object
    :param handle: Object returned from Task Validate

    :type threshold: float
    :param threshold: The threshold for disk usage percentage.

    :return: Status, result (if any exceeding the threshold).
    """

    # Request the allocation stats
    allocation_output = handle.web_request("/_cat/allocation?v", "GET", None)

    # Split the lines and skip the header
    lines = allocation_output.splitlines()[1:]

    # Calculate the max disk percentage from the lines, considering only assigned nodes
    max_disk_percent = 0  # Initialize to 0 or an appropriately low number
    for line in lines:
        if "UNASSIGNED" not in line:
            disk_usage = float(line.split()[5])
            max_disk_percent = max(max_disk_percent, disk_usage)
            if max_disk_percent > threshold:
                result = [{"usage_disk_percentage": max_disk_percent, "threshold": threshold}]
                return (False, result)      
    return (True, None)

