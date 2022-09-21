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
        
@beartype
def aws_list_attached_user_policies_printer(output):
    if output is None:
        return
    pprint.pprint(output)


@beartype
def aws_list_attached_user_policies(handle, UserName: str) -> List:
    """aws_list_attached_user_policies returns the list of policies attached to the user.

        :type UserName: string
        :param UserName: IAM user whose policies need to fetched.

        :rtype: List with with the attched policy names.
    """
    result = []
    ec2Client = handle.client('iam')
    try:
        response = ec2Client.list_attached_user_policies(UserName=UserName)
        for i in response["AttachedPolicies"]:
            result.append(i['PolicyName'])

    except ClientError as error:
        result.append(error.response)

    return result