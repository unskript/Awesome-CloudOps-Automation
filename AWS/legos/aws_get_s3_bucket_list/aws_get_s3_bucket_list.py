##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List
import pprint


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_get_s3_buckets_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_s3_buckets(handle, region: str) -> List:
    """aws_get_s3_buckets List all the S3 buckets.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: location of the bucket

        :rtype: List all the S3 buckets
    """
    # connect to the S3 using resource
    s3Session = handle.resource("s3", region_name=region)

    # Get all the S3 Buckets
    response = s3Session.buckets.all()
    result = []
    for bucket in response:
        result.append(bucket.name)
    return result
