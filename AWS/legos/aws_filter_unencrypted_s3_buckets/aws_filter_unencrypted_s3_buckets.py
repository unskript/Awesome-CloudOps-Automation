##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from botocore.exceptions import ClientError
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='AWS Region.')


def aws_filter_unencrypted_s3_buckets_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def aws_filter_unencrypted_s3_buckets(handle, region: str = "") -> Tuple:
    """aws_filter_unencrypted_s3_buckets List of unencrypted S3 bucket name .

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Filter S3 buckets.

        :rtype: Tuple with status result and list of unencrypted S3 bucket name.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            s3Client = handle.client('s3', region_name=reg)
            response = s3Client.list_buckets()
            # List unencrypted S3 buckets
            for bucket in response['Buckets']:
                try:
                    response = s3Client.get_bucket_encryption(Bucket=bucket['Name'])
                    encRules = response['ServerSideEncryptionConfiguration']['Rules']
                except ClientError as e:
                    bucket_dict = {}
                    bucket_dict["region"] = reg
                    bucket_dict["bucket"] = bucket['Name']
                    result.append(bucket_dict)
        except Exception as error:
            pass
    
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)

