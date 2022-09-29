##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List
import pprint


class InputSchema(BaseModel):
    bucket_list: list = Field(
        title='Bucket List',
        description='AWS S3 Bucket List.')

    permission: str = Field(
        title='Permission',
        description='ACL type - "READ"|"WRITE"|"READ_ACP"|"WRITE_ACP"|"FULL_CONTROL".')

    region: str = Field(
        title='Region',
        description='AWS Region.')
    
    
def aws_get_public_s3_buckets_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_public_s3_buckets(handle, bucket_list: list, permission: str, region: str) -> List:
    """aws_get_public_s3_buckets get list of public buckets.
        
        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type bucket_list: list
        :param bucket_list: list of S3 buckets.

        :type permission: string
        :param permission: ACL type - "READ"|"WRITE"|"READ_ACP"|"WRITE_ACP"|"FULL_CONTROL".

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
    for bucket in bucket_list:
        try:
            res = s3Client.get_bucket_acl(Bucket=bucket)
            for grant in res["Grants"]:
                if 'Permission' in grant.keys() and permission == grant["Permission"]:
                    if 'URI' in grant["Grantee"] and grant["Grantee"]["URI"] in public_check:
                        result.append(bucket)
        except Exception as e:
            continue

    return result