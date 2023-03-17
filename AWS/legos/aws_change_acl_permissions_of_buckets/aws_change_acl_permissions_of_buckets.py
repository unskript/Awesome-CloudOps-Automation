##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from unskript.enums.aws_canned_acl_enums import CannedACLPermissions
from typing import Optional, Dict
import pprint

class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')
    bucket_name: str = Field(
        title='Bucket Name',
        description='AWS S3 Bucket Name.')
    acl: Optional[CannedACLPermissions] = Field(
        title='Canned ACL Permission',
        description="Canned ACL Permission type - 'private'|'public-read'|'public-read-write'|'authenticated-read'.")


def aws_change_acl_permissions_of_buckets_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_change_acl_permissions_of_buckets(handle, bucket_name: str, acl: CannedACLPermissions=None, region: str = None) -> Dict:
    """ aws_put_bucket_acl get Dict of buckets ACL change info.

            :type handle: Session
            :param handle: Object returned by the task.validate(...) method
        
            :type bucket_name: string
            :param bucket_name: S3 bucket name where to set ACL on.

            :type acl: CannedACLPermissions
            :param acl: Canned ACL Permission type - 'private'|'public-read'|'public-read-write'|'authenticated-read'.

            :type region: string
            :param region: location of the bucket.

            :rtype: Dict of buckets ACL change info
    """
    # connect to the S3 using client
    all_permissions = acl
    if acl is None or len(acl)==0:
        all_permissions = "private"
    s3Client = handle.client('s3',
                             region_name=region)

    # Put bucket ACL for the permissions grant
    response = s3Client.put_bucket_acl(
                    Bucket=bucket_name,
                    ACL=all_permissions )

    return response
