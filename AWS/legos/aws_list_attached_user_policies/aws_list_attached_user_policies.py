##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
from botocore.exceptions import ClientError
import pprint


class InputSchema(BaseModel):
    user_name: str = Field(
        title='User Name',
        description='IAM user whose policies need to fetched.')
        

def aws_list_attached_user_policies_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_list_attached_user_policies(handle, user_name: str) -> List:
    """aws_list_attached_user_policies returns the list of policies attached to the user.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type user_name: string
        :param user_name: IAM user whose policies need to fetched.

        :rtype: List with with the attched policy names.
    """
    result = []
    ec2Client = handle.client('iam')
    try:
        response = ec2Client.list_attached_user_policies(UserName=user_name)
        for i in response["AttachedPolicies"]:
            result.append(i['PolicyName'])

    except ClientError as error:
        result.append(error.response)

    return result