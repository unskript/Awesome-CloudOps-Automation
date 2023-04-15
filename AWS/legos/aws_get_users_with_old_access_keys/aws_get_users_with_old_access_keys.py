##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field, SecretStr
from typing import Dict, List
from unskript.connectors.aws import aws_get_paginator
from datetime import datetime, timezone, timedelta
import pprint


class InputSchema(BaseModel):
    threshold_in_days: int = Field(
        default = 120,
        title="Threshold (In days)",
        description="(in days) The threshold to check the IAM user access keys older than the threshold."
    )


def aws_get_users_with_old_access_keys_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_users_with_old_access_keys(handle, threshold_in_days: int = 120) -> List:
    """aws_get_users_with_old_access_keys lists all the IAM users with access keys

        :type handle: object
        :param handle: Object returned from Task Validate
        
        :type threshold_in_days: int
        :param threshold_in_days: (in days) The threshold to check the IAM user access keys older than the threshold.

        :rtype: Result List of all IAM users with access keys.
    """
    client = handle.client('iam')
    result = []
    try:
        response = aws_get_paginator(client, "list_users", "Users")
    except Exception as e:
        return result.append({"error": e})
    for user in response:
        try:
            # Get a list of the user's access keys
            access_keys = client.list_access_keys(UserName=user['UserName'])
        except Exception as e:
            continue
        for access_key in access_keys['AccessKeyMetadata']:
            iam_data = {}
            try:
                access_key_info = client.get_access_key_last_used(AccessKeyId=access_key['AccessKeyId'])
            except Exception as e:
                continue
            if 'LastUsedDate' not in access_key_info['AccessKeyLastUsed']:
                iam_data["access_key"] = access_key['AccessKeyId']
                iam_data["iam_user"] = user['UserName']
                iam_data["last_used_days_ago"] = 'Never Used'
                result.append(iam_data)
            else:
                # Get the last used date of the access key
                last_used = access_key_info['AccessKeyLastUsed']['LastUsedDate']
                days_since_last_used = (datetime.now(timezone.utc) - last_used).days
                # Check if the access key was last used more than 90 days ago
                if days_since_last_used > threshold_in_days:
                    iam_data["access_key"] = access_key['AccessKeyId']
                    iam_data["iam_user"] = user['UserName']
                    iam_data["last_used_days_ago"] = days_since_last_used
                    result.append(iam_data)

    return result