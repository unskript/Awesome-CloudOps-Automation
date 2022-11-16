##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict
import pprint


class InputSchema(BaseModel):
    name: str = Field(
        title='Bucket Name',
        description='Name of the bucket.')
    enable_write: bool = Field(
        title='Enable write',
        description='Set this to true, if you want the bucket to be publicly writeable as well. By default, it is made publicly readable.')


def aws_make_bucket_public_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_make_bucket_public(handle, name: str, enable_write: bool) -> Dict:
    """aws_make_bucket_public Makes bucket public.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type name: string
        :param name: Name of the bucket.

        :type enable_write: bool
        :param enable_write: Set this to true for bucket to be publicly writeable.

        :rtype: Dict with information about the success of the request.
    """
    s3Client = handle.client('s3')

    acl = "public-read"
    if enable_write:
        acl = "public-read-write"
    res = s3Client.put_bucket_acl(Bucket=name, ACL=acl)
    return res
