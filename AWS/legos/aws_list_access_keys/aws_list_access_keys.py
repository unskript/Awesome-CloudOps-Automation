##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    aws_username: str = Field(
        title="Username",
        description="Username of the IAM User"
    )


def aws_list_access_keys_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_list_access_keys(
        handle,
        aws_username: str
) -> Dict:
    """aws_list_access_keys lists all the access keys for a user

        :type handle: object
        :param handle: Object returned from Task Validate

        :type aws_username: str
        :param aws_username: Username of the IAM user to be looked up

        :rtype: Result Dictionary of result
    """
    iamClient = handle.client('iam')
    result = iamClient.list_access_keys(UserName=aws_username)
    retVal = {}
    temp_list = []
    for key, value in result.items():
        if key not in temp_list:
            temp_list.append(key)
            retVal[key] = value
    return retVal
