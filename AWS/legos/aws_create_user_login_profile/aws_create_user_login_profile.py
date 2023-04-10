##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict
from botocore.exceptions import ClientError
import pprint


class InputSchema(BaseModel):
    user_name: str = Field(
        title='User Name',
        description='IAM User Name.')
    password: str = Field(
        title='Password',
        description='Password for IAM User.')


def aws_create_user_login_profile_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_create_user_login_profile(handle, user_name: str, password: str) -> Dict:
    """aws_create_user_login_profile Create login profile for IAM User.

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :type user_name: string
        :param user_name: Name of new IAM User.

        :type password: string
        :param password: temporary password for new User.

        :rtype: Dict with the Profile Creation status info.
    """

    ec2Client = handle.client("iam")
    result = {}
    try:
        response = ec2Client.create_login_profile(
            UserName=user_name,
            Password=password,
            PasswordResetRequired=True)

        result = response
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            result = error.response
        else:
            result = error.response

    return result