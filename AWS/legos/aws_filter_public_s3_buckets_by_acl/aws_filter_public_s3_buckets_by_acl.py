##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.legos.aws.aws_get_s3_buckets.aws_get_s3_buckets import aws_get_s3_buckets
from unskript.enums.aws_acl_permissions_enums import BucketACLPermissions


class InputSchema(BaseModel):
    region: Optional[str] = Field(
    default="",
    title='Region',
    description='Name of the AWS Region'
    )
    permission: Optional[BucketACLPermissions] = Field(
        default=BucketACLPermissions.READ,
        title="S3 Bucket's ACL Permission",
        description="Set of permissions that AWS S3 supports in an ACL for buckets and objects"
    )

def aws_filter_public_s3_buckets_by_acl_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def check_publicly_accessible_buckets(s3Client,b,all_permissions):
    public_check = ["http://acs.amazonaws.com/groups/global/AuthenticatedUsers",
                   "http://acs.amazonaws.com/groups/global/AllUsers"]
    public_buckets = False
    try:
        res = s3Client.get_bucket_acl(Bucket=b)
        for perm in all_permissions:
            for grant in res["Grants"]:
                if 'Permission' in grant.keys() and perm == grant["Permission"]:
                    if 'URI' in grant["Grantee"] and grant["Grantee"]["URI"] in public_check:
                        public_buckets = True
    except Exception:
        pass
    return public_buckets

def aws_filter_public_s3_buckets_by_acl(
        handle,
        permission:BucketACLPermissions=BucketACLPermissions.READ,
        region: str=None
        ) -> Tuple:
    """aws_filter_public_s3_buckets_by_acl get list of public buckets.
        
        Note- By default(if no permissions are given) READ and WRITE ACL Permissioned S3 buckets are
        checked for public access.Other ACL Permissions are - "READ_ACP"|"WRITE_ACP"|"FULL_CONTROL"
        :type handle: object
        :param handle: Object returned from task.validate(...)

        :type permission: Enum
        :param permission: Set of permissions that AWS S3 supports in an ACL for buckets and objects.

        :type region: string
        :param region: location of the bucket.
        
        :rtype: Object with status, list of public S3 buckets with READ/WRITE ACL Permissions, and errors
    """
    all_permissions = [permission]
    if permission is None or len(permission)==0:
        all_permissions = ["READ","WRITE"]
    result = []
    all_buckets = []
    all_regions = [region]
    if region is None or len(region)==0:
        all_regions = aws_list_all_regions(handle=handle)
    try:
        for r in all_regions:
            s3Client = handle.client('s3',region_name=r)
            output = aws_get_s3_buckets(handle=handle, region=r)
            if len(output)!= 0:
                for o in output:
                    all_buckets_dict = {}
                    all_buckets_dict["region"]=r
                    all_buckets_dict["bucket"]=o
                    all_buckets.append(all_buckets_dict)
    except Exception as e:
        raise e

    for bucket in all_buckets:
        s3Client = handle.client('s3',region_name= bucket['region'])
        flag = check_publicly_accessible_buckets(s3Client,bucket['bucket'], all_permissions)
        if flag:
            result.append(bucket)
    if len(result)!=0:
        return (False, result)
    else:
        return (True, None)
