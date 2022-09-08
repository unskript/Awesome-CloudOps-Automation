##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
from botocore.exceptions import ClientError
import pprint
from beartype import beartype


class InputSchema(BaseModel):
    user_name: str = Field(
        title='UserName',
        description='IAM User Name.')
    tag_key: str = Field(
        title='Tag Key',
        description='Tag Key to new IAM User.')
    tag_value: str = Field(
        title='Tag Value',
        description='Tag Value to new IAM User.')

@beartype
def aws_create_iam_user_printer(output):
    if output is None:
        return
    pprint.pprint(output)


@beartype
def aws_create_iam_user(handle, user_name: str, tag_key: str, tag_value: str) -> Dict:
    """aws_create_iam_user Creates new IAM User.

        :type handle: object
        :param handle: Object returned by the task.validate(...) method
        
        :type user_name: string
        :param user_name: Name of new IAM User.

        :type tag_key: string
        :param tag_key: Tag Key assign to new User.

        :type tag_value: string
        :param tag_value: Tag Value assign to new User.

        :rtype: Dict with the stopped instances state info.
    """

    ec2Client = handle.client("iam")
    result = {}
    try:
        response = ec2Client.create_user(
            UserName=user_name,
            Tags=[
                {
                    'Key': tag_key,
                    'Value': tag_value
                }])
        result = response
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            result = error.response
        else:
            result = error.response

    return result