##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict
import pprint


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')

    name: str = Field(
        title='Bucket Name',
        description='AWS S3 Bucket Name.')

def aws_delete_bucket_encryption_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_delete_bucket_encryption(handle, name: str, region: str) -> Dict:
    """aws_put_bucket_encryption Puts default encryption configuration for bucket.

          :type name: string
          :param name: Name of the S3 bucket.

          :type region: string
          :param region: location of the bucket

          :rtype: Dict with the response info.
      """
    s3Client = handle.client('s3',
                             region_name=region)
    
    result = {}

    # Setup default encryption configuration
    try:
        response = s3Client.delete_bucket_encryption(Bucket=name)

        result['Response'] = response

    except Exception as e:
        result['Error'] = e
        
    return result