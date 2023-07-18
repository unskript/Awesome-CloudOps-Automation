##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from google.cloud import storage


class InputSchema(BaseModel):
    age: int = Field(
        default=3,
        description='Age (in days) of bucket to add to lifecycle policy.',
        title='Age (in days)',
    )
    bucket_name: str = Field(
        description='GCP storage bucket name.', 
        title='Bucket Name'
    )


def gcp_add_lifecycle_policy_to_bucket_printer(output):
    if output is None:
        return
    print(output)

def gcp_add_lifecycle_policy_to_bucket(handle, bucket_name:str, age:int) -> str:
    """gcp_add_lifecycle_policy_to_bucket Returns the string of response of adding a lifecycle policy to a storage bucket

    :type handle: object
    :param handle: Object returned from Task Validate

    :type age: int
    :param age: Age (in days) of bucket to add to lifecycle policy.

    :type bucket_name: string
    :param bucket_name: GCP storage bucket name.

    :rtype: Response of adding a lifecycle policy to a storage bucket
    """
    storageClient = storage.Client(credentials= handle)

    bucket = storageClient.get_bucket(bucket_name)
    try:
        bucket.add_lifecycle_delete_rule(age=age)
    except Exception as e:
        raise e
    bucket.patch()
    return f"Added lifecycle policy to {bucket.name} which will delete object after {age} days of creation."


