##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field, SecretStr
from typing import Dict, List
import pprint


class InputSchema(BaseModel):
    aws_username: str = Field(
        title="Username",
        description="Username of the IAM User"
    )


def aws_create_access_key_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_create_access_key(
    handle,
    aws_username: str
) -> Dict:
    """aws_check_ssl_certificate_expiry checks the expiry date of an ACM SSL certificate .

            :type handle: object
            :param handle: Object returned from Task Validate

            :type aws_username: str
            :param aws_username: Username of the IAM user to be looked up

            :rtype: Result Dictionary of result
    """
    iamClient = handle.client('iam')
    result = iamClient.create_access_key(UserName=aws_username)
    return result
