##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field, SecretStr
from typing import Dict,List
from unskript.enums.aws_access_key_enums import AccessKeyStatus
import pprint


class InputSchema(BaseModel):
    aws_username: str = Field(
        title="Username",
        description="Username of the IAM User"
    )
    aws_access_key_id: str = Field(
        title="Access Key ID",
        description="Old Access Key ID of the User"
    )
    status: AccessKeyStatus = Field(
        title="Status",
        description="Status to set for the Access Key"
    )


def aws_update_access_key_printer(output):
    if output is None:
        return
    pprint.pprint("Access Key status successfully changed")
    pprint.pprint(output)


def aws_update_access_key(
    handle,
    aws_username: str,
    aws_access_key_id: str,
    status: AccessKeyStatus
) -> Dict:
    """aws_update_access_key updates the status of an access key to Inactive/Active
        :type handle: object
        :param handle: Object returned from Task Validate

        :type aws_username: str
        :param aws_username: Username of the IAM user to be looked up

        :type aws_access_key_id: str
        :param aws_access_key_id: Old Access Key ID of the user of which the status needs to be updated

        :type status: AccessKeyStatus
        :param status: Status to set for the Access Key

        :rtype: Result Dictionary of result
    """
    iamClient = handle.client('iam')
    result = iamClient.update_access_key(UserName=aws_username, AccessKeyId=aws_access_key_id, Status=status)
    retVal = {}
    temp_list = []
    for key, value in result.items():
        if key not in temp_list:
            temp_list.append(key)
            retVal[key] = value
    return retVal
