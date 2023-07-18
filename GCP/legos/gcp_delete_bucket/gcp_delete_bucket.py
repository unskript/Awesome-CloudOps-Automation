##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from beartype import beartype
import pprint
from typing import List,Any, Dict
from google.cloud import storage


class InputSchema(BaseModel):
    bucket_name: str = Field(
        title = "Bucket Name",
        description = "Name of the bucket to be deleted"
    )

def gcp_delete_bucket_printer(output):
    if output is None:
        return
    print(f"Bucket {output['deleted_bucket']} deleted")

def gcp_delete_bucket(handle, bucket_name: str) -> Dict:
    """gcp_delete_bucket Returns a Dict of details of the deleted bucket

        :type bucket_name: string
        :param bucket_name: Name of the bucket to be deleted

        :rtype: Dict of Bucket Details
    """
    result={}
    try:
        storage_client = storage.Client(credentials=handle)
        bucket = storage_client.get_bucket(bucket_name)
        result["deleted_bucket"]= bucket.name
        bucket.delete()
    except Exception as e:
        result["error"]= e
    return result