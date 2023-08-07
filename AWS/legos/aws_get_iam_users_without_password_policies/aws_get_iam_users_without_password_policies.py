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
    iam_client = handle.client('iam')
    paginator = iam_client.get_paginator('list_users')
    for response in paginator.paginate():
        for user in response['Users']:
            user_name = user['UserName']
            try:
                # Check for user-managed policies attached to the user
                user_policies = iam_client.list_user_policies(UserName=user_name)
                # Check for AWS-managed policies attached to the user
                attached_policies = iam_client.list_attached_user_policies(UserName=user_name)
                # If the user has no policies, add to result
                if not user_policies['PolicyNames'] and not attached_policies['AttachedPolicies']:
                    result.append(user_name)
            except Exception as e:
                print(f"An error occurred while processing user {user_name}: {e}")
    return (False, result) if result else (True, None)
