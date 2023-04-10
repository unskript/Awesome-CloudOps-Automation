##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.connectors.aws import aws_get_paginator
from datetime import datetime, timedelta
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint
import pytz


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='AWS Region.')
    max_age_days: Optional[int] = Field(
        default=30,
        title="Max Age Day's",
        description='The threshold to check the last use of the secret.')


def aws_list_unused_secrets_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_list_unused_secrets(handle, region: str = "", max_age_days: int = 30) -> Tuple:
    """aws_list_unused_secrets Returns an array of unused secrets.

        :type region: string
        :param region: AWS region.

        :type max_age_days: int
        :param max_age_days: The threshold to check the last use of the secret.

        :rtype: Tuple with status result and list of unused secrets.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            # Filtering the secrets by region
            ec2Client = handle.client('secretsmanager', region_name=reg)
            res = aws_get_paginator(ec2Client, "list_secrets", "SecretList")
            for secret in res:
                secret_dict = {}
                secret_id = secret['Name']
                last_accessed_date = ec2Client.describe_secret(SecretId=secret_id)
                if 'LastAccessedDate' in last_accessed_date:
                    if last_accessed_date["LastAccessedDate"] < datetime.now(pytz.UTC) - timedelta(days=int(max_age_days)):
                        secret_dict["secret_name"] = secret_id
                        secret_dict["region"] = reg
                        result.append(secret_dict)
                else:
                    if last_accessed_date["CreatedDate"] < datetime.now(pytz.UTC) - timedelta(days=int(max_age_days)):
                        secret_dict["secret_name"] = secret_id
                        secret_dict["region"] = reg
                        result.append(secret_dict)
        except Exception as e:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)