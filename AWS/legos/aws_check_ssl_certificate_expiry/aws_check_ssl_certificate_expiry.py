##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import dateutil
from pydantic import BaseModel, Field
from typing import Dict,List
import pprint
import datetime


class InputSchema(BaseModel):
    aws_certificate_arn: str = Field(
        title="Certificate ARN",
        description="ARN of the Certificate"
    )
    region: str = Field(
        title='Region',
        description='Name of the AWS Region'
    )


def aws_check_ssl_certificate_expiry_printer(output):
    if output is None:
        return
    if output > 0:
        pprint.pprint("Your SSL certificate is expiring in " + str(output) + " " + "days")
    else:
        pprint.pprint("Your SSL certificate has expired " + str(-output) + " " + "days ago")


def aws_check_ssl_certificate_expiry(
    handle,
    aws_certificate_arn: str,
    region: str,
) -> int:
    """aws_check_ssl_certificate_expiry checks the expiry date of an ACM SSL certificate .

            :type handle: object
            :param handle: Object returned from Task Validate

            :type aws_certificate_arn: str
            :param aws_certificate_arn: ARN of the certificate

            :type region: str
            :param region: Region name of the AWS account

            :rtype: Result Dictionary of result
    """
    iamClient = handle.client('acm', region_name=region)
    result = iamClient.describe_certificate(CertificateArn=aws_certificate_arn)
    for key,value in result['Certificate'].items():
        if key == "NotAfter":
            expiry_date = value
            right_now = datetime.datetime.now(dateutil.tz.tzlocal())
            diff = expiry_date-right_now
            days_remaining = diff.days
            if days_remaining < 30 and days_remaining > 0:
                days = days_remaining
            elif days_remaining < 0:
                days = days_remaining
            elif days_remaining > 30:
                days = days_remaining
            return days
