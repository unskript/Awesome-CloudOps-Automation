##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Optional, Tuple
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    threshold: Optional[float] = Field(
        83886080 , # 80GB in KB
        description='Threshold for disk size in KB.', 
        title='Threshold (in KB)'
    )


def mongodb_compare_disk_size_to_threshold_printer(output):
    success, alerts = output
    if success:
        print("Disk sizes are within the threshold.")
        return

    for alert in alerts:
        print(f"Alert! Disk size of {alert['totalDiskSize']} KB for database {alert['db']} exceeds threshold of {alert['threshold']} KB.")


def mongodb_compare_disk_size_to_threshold(handle, threshold: float=83886080) -> Tuple:
    """
    mongodb_compare_disk_size_to_threshold compares the total disk size used by MongoDB to a given threshold.

    :type handle: object
    :param handle: Object returned from Task Validate

    :type threshold: float
    :param threshold: The threshold for disk size in KB.

    :return: Status, a list of alerts if disk size is exceeded.
    """

    # Initialize variables
    total_disk_size = 0
    result = []

    # Get a list of database names
    database_names = handle.list_database_names()

    # Iterate through each database
    for db_name in database_names:
        db = handle[db_name]
        stats = db.command("dbStats")

        # Add the dataSize and indexSize to get the total size for the database
        total_disk_size = (stats['dataSize'] + stats['indexSize']) / (1024)

        if total_disk_size > threshold:
            # Append the database name, total disk size, and threshold to the result
            result.append({'db': db_name, 'totalDiskSize': total_disk_size, 'threshold': threshold})

    if len(result) != 0:
        return (False, result)
    return (True, None)



