# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import dateutil
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_iam_users.aws_list_all_iam_users import aws_list_all_iam_users
from unskript.legos.utils import CheckOutput, CheckOutputStatus
from typing import Dict,List,Tuple
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
    if isinstance(output, CheckOutput):
        print(output.json())
    else:
        pprint.pprint(output)

def aws_list_expiring_access_keys(handle, threshold_days: int)-> CheckOutput:
    """aws_list_expiring_access_keys returns all the ACM issued certificates which are about to expire given a threshold number of days

        :type handle: object
        :param handle: Object returned from Task Validate

        :type threshold_days: int
        :param threshold_days: Threshold number of days to check for expiry. Eg: 30 -lists all access Keys which are expiring within 30 days

        :rtype: Status, List of expiring access keys and Error if any 
    """
    result =[]
    all_users=[]
    try:
        all_users = aws_list_all_iam_users(handle=handle)
    except Exception as error:
        return CheckOutput(status=CheckOutputStatus.RUN_EXCEPTION,
                               objects=[],
                               error=error.__str__())
    for each_user in all_users:
        try:
            iamClient = handle.client('iam')
            final_result={}
            response = iamClient.list_access_keys(UserName=each_user)
            for x in response["AccessKeyMetadata"]:
                if len(response["AccessKeyMetadata"])!= 0:
                    create_date = x["CreateDate"]
                    right_now = datetime.datetime.now(dateutil.tz.tzlocal())
                    diff = right_now-create_date
                    days_remaining = diff.days
                    if days_remaining > threshold_days:
                        final_result["username"] = x["UserName"]
                        final_result["access_key_id"] = x["AccessKeyId"]
            if len(final_result)!=0:
                result.append(final_result)
        except Exception as e:
            return CheckOutput(status=CheckOutputStatus.RUN_EXCEPTION,
                               objects=[],
                               error=e.__str__())
    if len(result) != 0:
        return CheckOutput(status=CheckOutputStatus.FAILED,
                   objects=result,
                   error=str(""))
    else:
        return CheckOutput(status=CheckOutputStatus.SUCCESS,
                   objects=result,
                   error=str(""))