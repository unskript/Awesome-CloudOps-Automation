#
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
#
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
    acl: str = Field(
        title='ACL',
        description="canned ACL type - 'private'|'public-read'|'public-read-write'|'authenticated-read'.")


def aws_put_bucket_acl_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_put_bucket_acl(handle, bucket_name: str, acl: str, region: str = None) -> Dict:
    """ aws_put_bucket_acl apply ACL on s3 bucket.

            :type handle: Session
            :param handle: Object returned by the task.validate(...) method
        
            :type bucket_name: string
            :param bucket_name: S3 bucket name where to set ACL on.

            :type acl: str
            :param acl: canned ACL type - 'private'|'public-read'|'public-read-write'|'authenticated-read'.

            :type region: string
            :param region: location of the bucket.

            :rtype: ACL changed info as a Dict.
    """
    # connect to the S3 using client
    s3Client = handle.client('s3',
                             region_name=region)

    # Put bucket ACL for the permissions grant
    response = s3Client.put_bucket_acl(
                    Bucket=bucket_name,
                    ACL=acl )

    return response
