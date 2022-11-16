##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##  @author: Amit Chandak, @email: amit@unskript.com
##
from pydantic import BaseModel, Field
from typing import Dict
import json
import pprint


class InputSchema(BaseModel):
    name: str = Field(
        title='Bucket name',
        description='Name of the bucket.'
    )
    policy: str = Field(
        title='Bucket Policy',
        description='Bucket policy in JSON format.'
    )
    region: str = Field(
        title='Region',
        description='AWS region of the bucket.'
    )


def aws_put_bucket_policy_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_put_bucket_policy(handle, name: str, policy: str, region: str) -> Dict:
    """aws_put_bucket_policy Puts new policy for bucket.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :type name: string
          :param name: Name of the bucket.

          :type policy: string
          :param policy: Bucket policy in JSON format.

          :type region: string
          :param region: AWS region of the bucket.

          :rtype: Dict with the response info.
      """
    # Input param validation.

    s3Client = handle.client('s3',
                             region_name=region)

    # Setup a policy
    res = s3Client.put_bucket_policy(
        Bucket=name,
        Policy=json.dumps(policy)
    )
    return res['ResponseMetadata']
