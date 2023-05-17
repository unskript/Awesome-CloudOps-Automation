##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import pprint
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    bucketName: str = Field(
        title='Bucket',
        description='Name of the bucket to upload into.')
    file: str = Field(
        title='File',
        description='Name of the local file to upload into bucket. Eg /tmp/file-to-upload')
    prefix: str = Field(
        default="",
        title='Prefix',
        description='Prefix to attach to get the final object name to be used in the bucket.')


def aws_upload_file_to_s3_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_upload_file_to_s3(handle, bucketName: str, file: __file__, prefix: str = "") -> str:
    """aws_get_unhealthy_instances returns array of unhealthy instances

     :type handle: object
     :param handle: Object returned from task.validate(...).

     :type bucketName: string
     :param bucketName: Name of the bucket to upload into.

     :type file: __file__
     :param file: Name of the local file to upload into bucket.

     :type prefix: string
     :param prefix: Prefix to attach to get the final object name to be used in the bucket.

     :rtype: Returns array of unhealthy instances
    """
    s3 = handle.client('s3')
    objName = prefix + file.split("/")[-1]
    try:
        with open(file, "rb") as f:
            s3.upload_fileobj(f, bucketName, objName)
    except Exception as e:
        raise e
    return f"Successfully copied {file} to bucket:{bucketName} object:{objName}"
