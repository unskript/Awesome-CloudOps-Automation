# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import dateutil
from pydantic import BaseModel, Field
from typing import Dict,List
import pprint
import datetime

class InputSchema(BaseModel):
    threshold_days: int = Field(
        title="Threshold Days",
        description="Threshold number(in days) to check for expiry. Eg: 30 -lists all certificates which are expiring within 30 days"
    )
    region: str = Field(
        title='Region',
        description='Name of the AWS Region'
    )

def aws_list_expiring_acm_certificates_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_list_expiring_acm_certificates(handle, threshold_days: int, region: str='')-> Dict:
    """aws_list_expiring_acm_certificates returns all the ACM issued certificates which are about to expire given a threshold number of days

        :type handle: object
        :param handle: Object returned from Task Validate

        :type threshold_days: int
        :param threshold_days: Threshold number of days to check for expiry. Eg: 30 -lists all certificates which are expiring within 30 days

        :type region: str
        :param region: Region name of the AWS account

        :rtype: Result Dictionary of result
    """
    iamClient = handle.client('acm', region_name=region)
    arn_list=[]
    domain_list = []
    expiring_certificates_list= []
    expiring_certificates_dict={}
    result_list=[]
    try:
        certificates_list = iamClient.list_certificates(CertificateStatuses=['ISSUED'])
        for each_arn in certificates_list['CertificateSummaryList']:
            arn_list.append(each_arn['CertificateArn'])
            domain_list.append(each_arn['DomainName'])
        for cert_arn in arn_list:
            details = iamClient.describe_certificate(CertificateArn=cert_arn)
            for key,value in details['Certificate'].items():
                if key == "NotAfter":
                    expiry_date = value
                    right_now = datetime.datetime.now(dateutil.tz.tzlocal())
                    diff = expiry_date-right_now
                    days_remaining = diff.days
                    if days_remaining < threshold_days and days_remaining > 0:
                        expiring_certificates_list.append(cert_arn)
                    expiring_certificates_dict["region"]= region
                    expiring_certificates_dict["certificate"]= expiring_certificates_list
        result_list.append(expiring_certificates_dict)
    except Exception as e:
        pass
    return expiring_certificates_dict