# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Tuple
import datetime
import dateutil.tz
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_iam_users.aws_list_all_iam_users import aws_list_all_iam_users

class InputSchema(BaseModel):
    threshold_days: int = Field(
        default=90,
        title="Threshold Days",
        description="Threshold number(in days) to check for expiry. Eg: 30"
    )

def aws_list_expiring_access_keys_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_list_expiring_access_keys(handle, threshold_days: int = 90)-> Tuple:
    """aws_list_expiring_access_keys returns all the ACM issued certificates which are
       about to expire given a threshold number of days

        :type handle: object
        :param handle: Object returned from Task Validate

        :type threshold_days: int
        :param threshold_days: Threshold number of days to check for expiry. Eg: 30 -lists
        all access Keys which are expiring within 30 days

        :rtype: Status, List of expiring access keys and Error if any 
    """
    result = []
    all_users = []
    try:
        all_users = aws_list_all_iam_users(handle=handle)
    except Exception as error:
        raise error

    for each_user in all_users:
        try:
            iamClient = handle.client('iam')
            response = iamClient.list_access_keys(UserName=each_user)
            for x in response["AccessKeyMetadata"]:
                create_date = x["CreateDate"]
                right_now = datetime.datetime.now(dateutil.tz.tzlocal())
                diff = right_now - create_date
                days_remaining = threshold_days - diff.days
                if days_remaining >= 0 and days_remaining <= threshold_days:
                    final_result = {
                        "username": x["UserName"],
                        "access_key_id": x["AccessKeyId"]
                    }
                    result.append(final_result)
        except Exception as e:
            raise e

    if result:
        return (False, result)
    return (True, None)
