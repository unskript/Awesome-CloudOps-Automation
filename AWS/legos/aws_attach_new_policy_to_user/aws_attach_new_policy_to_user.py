##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
from botocore.exceptions import ClientError
import pprint
from beartype import beartype

class InputSchema(BaseModel):
    UserName: str = Field(
        title='User Name',
        description='IAM user whose policies need to fetched.')
    PolicyName: str = Field(
        title='Policy Name',
        description='Policy name to apply the permissions to the user.')

@beartype
def aws_attach_iam_policy_printer(output):
    if output is None:
        return
    pprint.pprint(output)


@beartype
def aws_attach_iam_policy(handle, UserName: str, PolicyName: str) -> Dict:
    """aws_attache_iam_policy used to provide user permissions.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type UserName: string
        :param UserName: Dictionary of credentials info.

        :type PolicyName: string
        :param PolicyName: Policy name to apply the permissions to the user.

        :rtype: Dict with User policy information.
    """
    result = {}
    iamResource = handle.resource('iam')
    try:
        user = iamResource.User(UserName)
        response = user.attach_policy(
            PolicyArn='arn:aws:iam::aws:policy/'+PolicyName
            )
        result = response
    except ClientError as error:
        result = error.response

    return result