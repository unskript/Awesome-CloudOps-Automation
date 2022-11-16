##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import io
from typing import List
from pydantic import BaseModel, Field
import pprint


class InputSchema(BaseModel):
    name: str = Field(
        title='Bucket Name',
        description='Name of the bucket of the object.')
    key: str = Field(
        title='Object Name',
        description='Name of S3 object or Prefix. Prefix should end with / to return the list of objects present in the bucket')


def aws_read_object_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_read_object(handle, name: str, key: str) -> List:
    """aws_read_object Reads object in S3.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type name: string
        :param name: Name of the bucket of the object.

        :type key: string
        :param key: Name of S3 object or Prefix.

        :rtype: List with the object data.
    """
    s3Client = handle.client('s3')
    if key.endswith("/"):
        folder_list = []
        res = s3Client.list_objects(Bucket=name, Prefix=key)
        print("\n")
        for content in res.get('Contents', []):
            print(content.get("Key"))
            folder_list.append(content.get("Key"))
        return folder_list
    elif key:
        res = s3Client.get_object(Bucket=name, Key=key)
        fileSizeLimit = 100000
        output = io.BytesIO(res['Body'].read()).read(fileSizeLimit).__str__()
        return [output]
