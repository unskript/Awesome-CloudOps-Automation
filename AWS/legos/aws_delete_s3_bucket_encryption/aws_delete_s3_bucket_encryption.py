##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')

    bucket_name: str = Field(
        title='Bucket Name',
        description='AWS S3 Bucket Name.')


def aws_delete_s3_bucket_encryption_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_delete_s3_bucket_encryption(handle, bucket_name: str, region: str) -> Dict:
    """aws_delete_s3_bucket_encryption Puts default encryption configuration for bucket.
        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :type bucket_name: string
        :param bucket_name: Name of the S3 bucket.

        :type region: string
        :param region: location of the bucket

        :rtype: Dict with the response info.
    """
    s3Client = handle.client('s3', region_name=region)
    
    result = {}

    # Setup default encryption configuration
    try:
        response = s3Client.delete_bucket_encryption(Bucket=bucket_name)

        result['Response'] = response

    except Exception as e:
        result['Error'] = e
        
    return result
