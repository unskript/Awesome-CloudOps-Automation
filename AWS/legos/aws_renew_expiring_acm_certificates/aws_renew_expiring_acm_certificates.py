# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import dateutil
from pydantic import BaseModel, Field
from typing import Dict,List
import pprint
import datetime

class InputSchema(BaseModel):
    aws_certificate_arn: List = Field(
        title="Certificate ARN",
        description="ARN of the Certificate"
    )
    region: str = Field(
        title='Region',
        description='Name of the AWS Region'
    )

def aws_renew_expiring_acm_certificates_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_renew_expiring_acm_certificates(handle, aws_certificate_arn: List, region: str='') -> Dict:
    """aws_renew_expiring_acm_certificates returns all the ACM issued certificates which are about to expire given a threshold number of days

        :type handle: object
        :param handle: Object returned from Task Validate

        :type aws_certificate_arn: List
        :param aws_certificate_arn: ARN of the Certificate

        :type region: str
        :param region: Region name of the AWS account

        :rtype: Result Dictionary of result
    """
    result = {}
    try:
        acmClient = handle.client('acm', region_name=region)
        for arn in aws_certificate_arn:
            acmClient.renew_certificate(CertificateArn=arn)
            result[arn] = "Successfully renewed"
    except Exception as e:
        result["error"] = e
    return result