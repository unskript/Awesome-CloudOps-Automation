# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import dateutil
from pydantic import BaseModel, Field
from typing import Dict,List
import pprint
import datetime

class InputSchema(BaseModel):
    aws_username: str = Field(
        title="Username",
        description="Username of the IAM User"
    )
    threshold_days: int = Field(
        title="Threshold Days",
        description="Threshold number(in days) to check for expiry. Eg: 30"
    )

def aws_list_expiring_access_keys_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_list_expiring_access_keys(handle, threshold_days: int, aws_username: str='')-> Dict:
    """aws_list_expiring_access_keys returns all the ACM issued certificates which are about to expire given a threshold number of days

        :type handle: object
        :param handle: Object returned from Task Validate

        :type threshold_days: int
        :param threshold_days: Threshold number of days to check for expiry. Eg: 30 -lists all access Keys which are expiring within 30 days

        :type aws_username: str
        :param aws_username: Username of the IAM User

        :rtype: Result Dictionary of result
    """
    try:
        iamClient = handle.client('iam')
        response = iamClient.list_access_keys(UserName=aws_username)
        result = {}
        for x in response["AccessKeyMetadata"]:
            if len(response["AccessKeyMetadata"])!= 0:
                create_date = x["CreateDate"]
                right_now = datetime.datetime.now(dateutil.tz.tzlocal())
                diff = right_now-create_date
                days_remaining = diff.days
                if days_remaining > threshold_days:
                    result["username"] = x["UserName"]
                    result["access_key_id"] = x["AccessKeyId"]
    except Exception as e:
        result["error"] = e
    return result