##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict
from botocore.exceptions import ClientError
import pprint

from beartype import beartype

class InputSchema(BaseModel):
    UserName: str = Field(
        title='UserName',
        description='IAM User Name.')
    Password: str = Field(
        title='Password',
        description='Password for IAM User.')

@beartype
def aws_create_user_login_profile_printer(output):
    if output is None:
        return
    pprint.pprint(output)


@beartype
def aws_create_user_login_profile(handle, UserName: str, Password: str) -> Dict:
    """aws_create_user_login_profile Create login profile for IAM User.

        :type UserName: string
        :param UserName: Name of new IAM User.

        :type Password: string
        :param Password: temporary password for new User.

        :rtype: Dict with the Profile Creation status info.
    """

    ec2Client = handle.client("iam")
    result = {}
    try:
        response = ec2Client.create_login_profile(
            UserName=UserName,
            Password=Password,
            PasswordResetRequired=True)

        result = response
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            result = error.response
        else:
            result = error.response

    return result