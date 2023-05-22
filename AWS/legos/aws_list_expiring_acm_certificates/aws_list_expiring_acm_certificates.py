# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Optional,Tuple
import datetime
import dateutil
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions

class InputSchema(BaseModel):
    threshold_days: int = Field(
        title="Threshold Days",
        description=("Threshold number(in days) to check for expiry. "
                     "Eg: 30 -lists all certificates which are expiring within 30 days")
    )
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='Name of the AWS Region'
    )

def aws_list_expiring_acm_certificates_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_list_expiring_acm_certificates(handle, threshold_days: int = 90, region: str=None)-> Tuple:
    """aws_list_expiring_acm_certificates returns all the ACM issued certificates which
       are about to expire given a threshold number of days

        :type handle: object
        :param handle: Object returned from Task Validate

        :type threshold_days: int
        :param threshold_days: Threshold number of days to check for expiry.
        Eg: 30 -lists all certificates which are expiring within 30 days

        :type region: str
        :param region: Region name of the AWS account

        :rtype: Tuple containing status, expiring certificates, and error
    """
    arn_list=[]
    domain_list = []
    expiring_certificates_list= []
    expiring_certificates_dict={}
    result_list=[]
    all_regions = [region]
    if region is None or len(region)==0:
        all_regions = aws_list_all_regions(handle=handle)
    for r in all_regions:
        iamClient = handle.client('acm', region_name=r)
        try:
            expiring_certificates_dict={}
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
                        if 0 < days_remaining < threshold_days:
                            expiring_certificates_list.append(cert_arn)
            expiring_certificates_dict["region"]= r
            expiring_certificates_dict["certificate"]= expiring_certificates_list
            if len(expiring_certificates_list)!=0:
                result_list.append(expiring_certificates_dict)
        except Exception:
            pass
    if len(result_list)!=0:
        return (False, result_list)
    return (True, None)
