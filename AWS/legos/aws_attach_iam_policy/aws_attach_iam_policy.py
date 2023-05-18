##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field
from botocore.exceptions import ClientError


class InputSchema(BaseModel):
    user_name: str = Field(
        title='User Name',
        description='IAM user whose policies need to fetched.')
    policy_name: str = Field(
        title='Policy Name',
        description='Policy name to apply the permissions to the user.')


def aws_attach_iam_policy_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_attach_iam_policy(handle, user_name: str, policy_name: str) -> Dict:
    """aws_attache_iam_policy used to provide user permissions.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type user_name: string
        :param user_name: Dictionary of credentials info.

        :type policy_name: string
        :param policy_name: Policy name to apply the permissions to the user.

        :rtype: Dict with User policy information.
    """
    result = {}
    iamResource = handle.resource('iam')
    try:
        user = iamResource.User(user_name)
        response = user.attach_policy(
            PolicyArn='arn:aws:iam::aws:policy/'+policy_name
            )
        result = response
    except ClientError as error:
        result = error.response

    return result
