##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
import pprint
from typing import List,Any, Dict
from google.cloud import storage
from google.cloud.storage import bucket

class InputSchema(BaseModel):
    pass

def gcp_list_public_buckets_printer(output):
    if len(output)==0:
        print("There are no publicly readable buckets available")
        return
    print(output)
    

def gcp_list_public_buckets(handle) -> List:
    """gcp_list_public_buckets lists all public GCP Buckets

        :rtype: List of all public GCP buckets
    """
    try:
        storage_client = storage.Client(credentials=handle)
        buckets = storage_client.list_buckets()
        result = []
        for bucket in buckets:
            l = str(bucket.name)
            b = storage_client.bucket(l)
            policy = b.get_iam_policy(requested_policy_version=3)
            for binding in policy.bindings:
                if binding['members']=={'allUsers'}:
                        result.append(bucket.name)
    except Exception as e:
        result["error"]= e
    return result