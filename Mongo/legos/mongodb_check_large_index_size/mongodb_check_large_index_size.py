##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Tuple, Optional
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    index_threshold: Optional[float] = Field(
        2048000,  # 2GB in KB
        description='The threshold for total index size. Default is 512000KB.',
        title='Index threshold(in KB)',
    )



def mongodb_check_large_index_size_printer(output):
    success, alerts = output
    if success:
        print("Index sizes are within the threshold.")
        return

    # Otherwise, print the alerts
    for alert in alerts:
        print(f"Alert! Index size of {alert['indexSizeKB']} KB for database '{alert['db']}' in collection '{alert['collection']}' exceeds threshold !")


def mongodb_check_large_index_size(handle, threshold: float = 2048000) -> Tuple:
    """
    mongodb_check_large_index_size checks the index sizes for all databases and collections.
    It compares the size of each index with a given threshold and returns any indexes that exceed the threshold.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :type threshold: float
    :param threshold: The threshold for index size in KB

    :rtype: Status, the list of the details of the indexes that exceeded the threshold.
    """

    # List to hold alerts for indexes that exceed the threshold
    alerts = []

    try:
        database_names = [db for db in handle.list_database_names() if db != 'local']
        for db_name in database_names:
            db = handle[db_name]
            collection_names = db.list_collection_names()
            # Iterate through each collection in the database
            for coll_name in collection_names:
                coll = db.get_collection(coll_name)
                # Skip views
                if coll.options().get('viewOn'):
                    continue

                stats = db.command("collstats", coll_name)
                # Check each index's size
                for index_name, index_size in stats['indexSizes'].items():
                    index_size_KB = index_size / 1024  # Convert to KB

                    if index_size_KB > threshold:
                        alerts.append({
                            'db': db_name,
                            'collection': coll_name,
                            'index': index_name,
                            'indexSizeKB': index_size_KB
                        })
    
    except Exception as e:
        raise e
        
    if len(alerts) != 0:
        return (False, alerts)
    return (True, None)




