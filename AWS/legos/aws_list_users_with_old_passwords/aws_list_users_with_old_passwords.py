##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from dateutil.parser import parse
from unskript.connectors.aws import aws_get_paginator


class InputSchema(BaseModel):
    threshold_days: int = Field(
        default = 120,
        title='Threshold (In days)',
        description=('(in days) The threshold to check the IAM user '
                     'password older than the threshold.')
                    )

def aws_list_users_with_old_passwords_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_list_users_with_old_passwords(handle, threshold_days: int = 120) -> List:
    """aws_list_users_with_old_passwords lists all the IAM users with old passwords.

        :type handle: object
        :param handle: Object returned from Task Validate

        :type threshold_days: int
        :param threshold_days: (in days) The threshold to check the IAM user
        password older than the threshold.

        :rtype: Result List of all IAM users
    """
    client = handle.client('iam')
    users_list = []
    now = datetime.now(timezone.utc)
    response = aws_get_paginator(client, "list_users", "Users")
    for user in response:
        try:
            login_profile = client.get_login_profile(UserName=user['UserName'])
            if 'CreateDate' in login_profile['LoginProfile']:
                password_last_changed = parse(
                    str(login_profile['LoginProfile']['CreateDate'])
                    ).replace(tzinfo=timezone.utc)
                password_age = now - password_last_changed
                if password_age > timedelta(days=threshold_days):
                    users_list.append(user['UserName'])
        except Exception:
            pass

    if len(users_list) != 0:
        return (False, users_list)
    return (True, None)
