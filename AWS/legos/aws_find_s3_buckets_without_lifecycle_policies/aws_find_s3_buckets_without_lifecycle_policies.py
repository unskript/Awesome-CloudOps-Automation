##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.legos.aws.aws_get_s3_buckets.aws_get_s3_buckets import aws_get_s3_buckets
from typing import List, Optional, Tuple
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field('', description='AWS Region of S3 buckets.', title='Region')



def aws_find_s3_buckets_without_lifecycle_policies_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_find_s3_buckets_without_lifecycle_policies(handle, region: str="") -> Tuple:
    """aws_find_s3_buckets_without_lifecycle_policies List all the S3 buckets without lifecycle policies

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: AWS Region of the bucket

        :rtype: Status, List of all the S3 buckets without lifecycle policies with regions
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            s3Session = handle.resource("s3", region_name=reg)
            response = aws_get_s3_buckets(handle, region=reg)
            for bucket in response:
                bucket_region = s3Session.meta.client.get_bucket_location(Bucket=bucket)['LocationConstraint']
                if bucket_region is None:
                    bucket_region = 'us-east-1'
                if bucket_region != reg:
                    continue
                bucket_lifecycle_configuration = s3Session.BucketLifecycleConfiguration(bucket)
                try:
                    if bucket_lifecycle_configuration.rules:
                        continue
                except Exception:
                    bucket_details = {}
                    bucket_details["bucket_name"] = bucket
                    bucket_details["region"] = reg
                    result.append(bucket_details)
        except Exception:
            pass
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)


