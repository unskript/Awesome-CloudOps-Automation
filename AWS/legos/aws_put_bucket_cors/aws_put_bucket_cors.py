##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
# @author: Yugal Pachpande, @email: yugal.pachpande@unskript.com
##
import pprint
from pydantic import BaseModel, Field
from typing import Any, Dict, List


class InputSchema(BaseModel):
    name: str = Field(
        title='Bucket name',
        description='Name of the bucket.'
    )
    corsRules: List[Dict[str, Any]] = Field(
        title='Bucket Policy',
        description='cross-origin access configuration in JSON format. eg. [{"AllowedHeaders":["*"],"AllowedMethods":["PUT","POST","DELETE"],"AllowedOrigins":["http://www.example1.com" ],"ExposeHeaders": []}, {"AllowedHeaders": [],"AllowedMethods":["GET"],"AllowedOrigins":["*"],"ExposeHeaders":[]}]'
    )
    region: str = Field(
        title='Region',
        description='AWS region of the bucket.'
    )


def aws_put_bucket_cors_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_put_bucket_cors(handle, name: str, corsRules: List, region: str) -> Dict:
    """aws_put_bucket_cors Puts CORS policy for bucket.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :type name: string
          :param name: Name of the bucket.

          :type corsRules: list
          :param corsRules: cross-origin access configuration in JSON format.

          :type region: string
          :param region: AWS region of the bucket.

          :rtype: Dict with the response info.
      """
    # Input param validation.

    s3Client = handle.client('s3', region_name=region)

    cors_configuration = {'CORSRules': corsRules}
    pprint.pprint("Applying config to bucket: %s" % str(cors_configuration))

    # Setup a CORS policy
    res = s3Client.put_bucket_cors(
        Bucket=name,
        CORSConfiguration=cors_configuration
    )
    return res
