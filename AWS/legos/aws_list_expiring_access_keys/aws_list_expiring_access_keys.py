# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import dateutil
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_iam_users.aws_list_all_iam_users import aws_list_all_iam_users
from typing import Dict,List
import pprint
import datetime

class InputSchema(BaseModel):
    threshold_days: int = Field(
        title="Threshold Days",
        description="Threshold number(in days) to check for expiry. Eg: 30"
    )

def aws_list_expiring_access_keys_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_list_expiring_access_keys(handle, threshold_days: int)-> List:
    """aws_list_expiring_access_keys returns all the ACM issued certificates which are about to expire given a threshold number of days

        :type handle: object
        :param handle: Object returned from Task Validate

        :type threshold_days: int
        :param threshold_days: Threshold number of days to check for expiry. Eg: 30 -lists all access Keys which are expiring within 30 days

        :rtype: Result Dictionary of result
    """
    final_result=[]
    all_users=[]
    try:
        all_users = aws_list_all_iam_users(handle=handle)
    except Exception as error:
        pass
    for each_user in all_users:
        try:
            iamClient = handle.client('iam')
            result = {}
            response = iamClient.list_access_keys(UserName=each_user)
            for x in response["AccessKeyMetadata"]:
                if len(response["AccessKeyMetadata"])!= 0:
                    create_date = x["CreateDate"]
                    right_now = datetime.datetime.now(dateutil.tz.tzlocal())
                    diff = right_now-create_date
                    days_remaining = diff.days
                    if days_remaining > threshold_days:
                        result["username"] = x["UserName"]
                        result["access_key_id"] = x["AccessKeyId"]
            if len(result)!=0:
                final_result.append(result)
        except Exception as e:
            pass
    return final_result