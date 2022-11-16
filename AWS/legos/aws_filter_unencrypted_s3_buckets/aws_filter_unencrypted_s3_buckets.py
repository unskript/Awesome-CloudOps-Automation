##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List
from botocore.exceptions import ClientError
import pprint


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_filter_unencrypted_s3_buckets_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_filter_unencrypted_s3_buckets(handle, region: str) -> List:
    """aws_filter_unencrypted_s3_buckets List of unencrypted bucket name .

        :type handle: object
        :param handle: Object returned from task.validate(...).
        
        :type region: string
        :param region: Filter S3 buckets.

        :rtype: List with unencrypted bucket name.
    """
    s3Client = handle.client('s3',
                             region_name=region)

    response = s3Client.list_buckets()

    # List unencrypted S3 buckets
    result = []
    for bucket in response['Buckets']:
        try:
            response = s3Client.get_bucket_encryption(Bucket=bucket['Name'])
            encRules = response['ServerSideEncryptionConfiguration']['Rules']

        except ClientError as e:
            result.append(bucket['Name'])

    return result

