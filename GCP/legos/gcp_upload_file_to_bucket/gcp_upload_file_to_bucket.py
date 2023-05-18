##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import Dict
from pydantic import BaseModel, Field
from google.cloud import storage


class InputSchema(BaseModel):
    blob_name: str = Field(
        title = "Blob Name",
        description = "Name of the object/blob to be created"
    )
    bucket_name: str = Field(
        title = "Bucket Name",
        description = "Name of the bucket to create object/blob"
    )
    data: str = Field(
        title = "Input Data",
        description = "String of data to be added to the object/blob"
    )

def gcp_upload_file_to_bucket_printer(output):
    if output is None:
        return
    print(f"Created an object {output['blob_name']} in {output['bucket_name']} bucket")


def gcp_upload_file_to_bucket(handle,blob_name: str, bucket_name: str, data: str) -> Dict:
    """gcp_upload_file_to_bucket returns a List of objects in the Bucket

        :type blob_name: string
        :param bucket_name: Name of the object/blob to be created

        :type bucket_name: string
        :param bucket_name:Name of the bucket to create object/blob

        :type data: string
        :param bucket_name: String of data to be added to the object/blob

        :rtype: Dict of blob details
    """
    try:
        result = {}
        storage_client = storage.Client(credentials=handle)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob = blob.upload_from_string(data)
        result["blob_name"] = blob_name
        result["bucket_name"] = bucket_name
    except Exception as e:
        result["error"]= e
    return result
