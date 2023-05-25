##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List
from pydantic import BaseModel, Field
from google.cloud import storage


class InputSchema(BaseModel):
    bucket_name: str = Field(
        title = "Bucket Name",
        description = "Name of the bucket to be deleted"
    )

def gcp_fetch_objects_from_bucket_printer(output):
    if len(output)==0:
        print("Bucket is empty")
        return
    for blob in output:
        print(blob)

def gcp_fetch_objects_from_bucket(handle, bucket_name: str) -> List:
    """gcp_fetch_objects_from_bucket returns a List of objects in the Bucket

        :type bucket_name: string
        :param bucket_name: Name of the bucket to fetch objects/blobs from

        :rtype: List of Bucket Objects
    """
    try:
        result =[]
        storage_client = storage.Client(credentials=handle)
        bucket = storage_client.get_bucket(bucket_name)
        blobs = bucket.list_blobs()
        for blob in blobs:
            result.append(blob)
    except Exception as e:
        result["error"]= e
    return result
