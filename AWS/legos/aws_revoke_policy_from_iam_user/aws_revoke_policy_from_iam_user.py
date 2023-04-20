##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict
import pprint


class InputSchema(BaseModel):
    user_name: str = Field(
        title='User Name',
        description='The name of the IAM user from whom to revoke the policy.')
    policy_arn: str = Field(
        title='Policy ARNs',
        description='The Amazon Resource Name (ARN) of the policy.')


def aws_revoke_policy_from_iam_user_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_revoke_policy_from_iam_user(handle, user_name: str, policy_arn: str) -> Dict:
    """aws_revoke_policy_from_iam_user revoke policy from iam user.

        :type handle: object
        :param handle: Object returned from Task Validate

        :type policy_arn: str
        :param policy_arn: The Amazon Resource Name (ARN) of the policy.

        :type user_name: str
        :param user_name: The name of the IAM user from whom to revoke the policy.

        :rtype: Dict
    """
    try:
        client = handle.client('iam')
        response = client.detach_user_policy(
                            UserName=user_name,
                            PolicyArn=policy_arn)
        return response
    except Exception as e:
        raise Exception(e)
