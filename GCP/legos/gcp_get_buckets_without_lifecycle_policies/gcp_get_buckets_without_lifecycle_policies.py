##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import List, Tuple
from pydantic import BaseModel, Field
from google.cloud import storage


class InputSchema(BaseModel):
    pass


def gcp_get_buckets_without_lifecycle_policies_printer(output):
    if output is None:
        return
    print(output)

def gcp_get_buckets_without_lifecycle_policies(handle) -> Tuple:
    """gcp_get_buckets_without_lifecycle_policies Returns the List of GCP storage buckets without lifecycle policies

    :type handle: object
    :param handle: Object returned from Task Validate

    :rtype: Tuple of storage buckets without lifecycle policies and the corresponding status.
    """
    try:
        storageClient = storage.Client(credentials=handle)
        buckets = storageClient.list_buckets()
        result = []
        for bucket in buckets:
            if not list(bucket.lifecycle_rules):
                result.append(bucket.name)
        if result:
            return (False, result)
        return (True, None)
    except Exception as e:
        raise e


