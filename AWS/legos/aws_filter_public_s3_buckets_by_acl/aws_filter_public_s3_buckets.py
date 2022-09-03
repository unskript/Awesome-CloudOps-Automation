##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')
    Bucket_List: list = Field(
        title='Bucket List',
        description='AWS S3 Bucket List.')
    Permission: str = Field(
        title='Permission',
        description='ACL type - "READ"|"WRITE"|"READ_ACP"|"WRITE_ACP"|"FULL_CONTROL".')



def aws_get_public_s3_buckets_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_public_s3_buckets(handle, Bucket_List: list, Permission: str, region: str) -> List:
    """aws_get_public_s3_buckets get list of public buckets.

          :type Bucket_List: list
          :param Bucket_List: list of S3 buckets.

          :type region: string
          :param region: location of the bucket.

          :rtype: Dict with the response info.
      """
    # connect to the S3 using client
    s3Client = handle.client('s3',
                             region_name=region)
    public_check = ["http://acs.amazonaws.com/groups/global/AuthenticatedUsers",
                   "http://acs.amazonaws.com/groups/global/AllUsers"]
    # filter public S3 buckets
    result = []
    for bucket in Bucket_List:
        try:
            res = s3Client.get_bucket_acl(Bucket=bucket)
            for grant in res["Grants"]:
                if 'Permission' in grant.keys() and Permission == grant["Permission"]:
                    if 'URI' in grant["Grantee"] and grant["Grantee"]["URI"] in public_check:
                        result.append(bucket)
        except Exception:
            continue

    return result
