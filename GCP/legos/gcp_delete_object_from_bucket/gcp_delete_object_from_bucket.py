##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict
from google.cloud import storage

class InputSchema(BaseModel):
    blob_name: str = Field(
        title = "Blob Name",
        description = "Name of the object/blob to be deleted"
    )
    bucket_name: str = Field(
        title = "Bucket Name",
        description = "Name of the bucket to delete object/blob from"
    )

def gcp_delete_object_from_bucket_printer(output):
    if output is None:
        return
    print(f"Successfully deleted {output['blob_name']}")


def gcp_delete_object_from_bucket(handle,blob_name: str, bucket_name: str) -> Dict:
    """gcp_delete_object_from_bucket deletes an object in a GCP Bucket

        :type blob_name: string
        :param bucket_name: Name of the object/blob to be deleted

        :type bucket_name: string
        :param bucket_name:Name of the bucket to delete object/blob from

        :rtype: Dict of deleted blob
    """
    try:
        result={}
        storage_client = storage.Client(credentials=handle)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()
        result["blob_name"]= blob_name
    except Exception as e:
        result["error"]= e
    return result