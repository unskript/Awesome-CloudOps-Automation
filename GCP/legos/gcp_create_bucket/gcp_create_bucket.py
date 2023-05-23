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
        description = "Name of the bucket to be created"
    )
    project_name: str = Field(
        '',
        title = "GCP Project",
        description = "GCP Project Name"
    )
    storage_class: str = Field(
        'STANDARD',
        title = "Storage Class",
        description = "Storage class to be assigned to the new bucket. Eg- STANDARD, COLDLINE"
    )
    location: str = Field(
        'us',
        title = "Location",
        description = "GCP location where bucket should be created. Eg- US"
    )

def gcp_create_bucket_printer(output):
    if output is None:
        return
    print(f"Created bucket {output['name']} in {output['location']} with storage class {output['location']}")

def gcp_create_bucket(handle, bucket_name: str, location: str, project_name: str,storage_class: str) -> Dict:
    """gcp_create_bucket Returns a Dict of details of the newly created bucket

        :type bucket_name: string
        :param bucket_name: Name of the bucket to be created

        :type project_name: string
        :param project_name: GCP Project Name

        :type storage_class: string
        :param storage_class: Storage class to be assigned to the new bucket

        :type location: string
        :param location: GCP location where bucket should be created

        :rtype: Dict of Bucket Details
    """
    result={}
    try:
        storage_client = storage.Client(credentials=handle)
        bucket = storage_client.bucket(bucket_name)
        bucket.storage_class = storage_class
        new_bucket = storage_client.create_bucket(bucket,location=location, project=project_name)
        result["name"]= new_bucket.name
        result["location"]= new_bucket.location
        result["storage_class"]= new_bucket.storage_class
    except Exception as e:
        result["error"]= e
    return result