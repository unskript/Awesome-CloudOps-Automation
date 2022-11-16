##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Dict
import pprint
from unskript.legos.aws.aws_get_handle.aws_get_handle import Session


class InputSchema(BaseModel):
    name: str = Field(
        title='Bucket Name',
        description='Name of the bucket to be deleted.')
    region: Optional[str] = Field(
        title='Region',
        description='AWS Region of the bucket.')


def aws_delete_bucket_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_delete_bucket(handle: Session, name: str, region: str = None) -> Dict:
    """aws_delete_bucket Deletes a bucket.
        :type handle: object
        :param handle: Object returned from Task Validate

        :type name: string
        :param name: Name of the bucket to be deleted.

        :type region: string
        :param region: AWS Region of the bucket.

        :rtype: Dict with the deleted bucket info.
    """

    if region is None:
        s3Client = handle.client('s3')
    else:
        s3Client = handle.client('s3', region_name=region)

    res = s3Client.delete_bucket(Bucket=name)
    return res
