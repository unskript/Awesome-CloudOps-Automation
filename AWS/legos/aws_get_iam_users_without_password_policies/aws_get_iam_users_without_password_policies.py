##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Tuple
from unskript.legos.aws.aws_list_all_iam_users.aws_list_all_iam_users import aws_list_all_iam_users
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    pass



def aws_get_iam_users_without_password_policies_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_iam_users_without_password_policies(handle) -> Tuple:
    """aws_get_iam_users_without_password_policies lists all the IAM users no password policy.

        :type handle: object
        :param handle: Object returned from Task Validate

        :rtype: Status, List of IAM users without any password policy
    """
    result = []
    iamClient = handle.client('iam')
    response = aws_list_all_iam_users(handle)
    for user in response:
        try:
            iamClient.get_account_password_policy()
        except iamClient.exceptions.NoSuchEntityException:
            result.append(user)
    if len(result) != 0:
        return (False, result)
    return (True, None)

