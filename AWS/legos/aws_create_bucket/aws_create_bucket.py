##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Optional, Dict
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_get_handle.aws_get_handle import Session


class InputSchema(BaseModel):
    name: str = Field(
        title='Bucket Name',
        description='Name of the bucket to be created.')
    acl: str = Field(
        title='ACL',
        description=('The Canned ACL to apply to the bucket. Possible values: '
                     'private, public-read, public-read-write, authenticated-read.')
    region: Optional[str] = Field(
        title='Region',
        description='AWS Region of the bucket.')


def aws_create_bucket_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_create_bucket(handle: Session, name: str, acl: str, region: str = None) -> Dict:
    """aws_create_bucket Creates a new bucket.

        :rtype: Dict with the new bucket info.
    """
    # Input param validation.
    if region is None:
        s3Client = handle.client('s3')
        res = s3Client.create_bucket(
            ACL=acl,
            Bucket=name)
    else:
        s3Client = handle.client('s3', region_name=region)
        res = s3Client.create_bucket(
            ACL=acl,
            Bucket=name,
            CreateBucketConfiguration={
                'LocationConstraint': region})
    return res
