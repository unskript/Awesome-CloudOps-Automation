##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel
from google.cloud import storage

class InputSchema(BaseModel):
    pass

def gcp_list_buckets_printer(output):
    if len(output)==0:
        print("There are no buckets available")
        return
    pprint.pprint(output)


def gcp_list_buckets(handle) -> List:
    """gcp_list_buckets lists all GCP Buckets

        :rtype: List of all GCP buckets
    """
    try:
        result=[]
        storage_client = storage.Client(credentials=handle)
        buckets = storage_client.list_buckets()
        for bucket in buckets:
            result.append(bucket.name)
    except Exception as e:
        raise e
    return result
