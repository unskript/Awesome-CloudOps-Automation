##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict, Optional
import pprint


class InputSchema(BaseModel):
    region: str = Field(
        description='AWS Region.', 
        title='Region')
    bucket_name: str = Field(
        description='The name of the bucket for which to set the configuration.',
        title='Bucket Name',
    )
    expiration_days: Optional[float] = Field(
        30,
        description='Specifies the expiration for the lifecycle of the object in the form of days. Eg: 30 (days)',
        title='Expiration Days',
    )
    prefix: Optional[str] = Field(
        '',
        description='Prefix identifying one or more objects to which the rule applies.',
        title='Prefix',
    )
    noncurrent_days: Optional[float] = Field(
        30,
        description='Specifies the number of days an object is noncurrent before Amazon S3 permanently deletes the noncurrent object versions',
        title='Noncurrent Days',
    )



def aws_add_lifecycle_configuration_to_s3_bucket_printer(output):
    if output is None:
        return
    pprint.pprint(output)



def aws_add_lifecycle_configuration_to_s3_bucket(handle, region: str, bucket_name:str, expiration_days:int=30, prefix:str='', noncurrent_days:int=30) -> Dict:
    """aws_add_lifecycle_configuration_to_s3_bucket returns response of adding lifecycle configuration

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: location of the bucket
        
        :type bucket_name: string
        :param bucket_name: The name of the bucket for which to set the configuration.

        :type expiration_days: int
        :param expiration_days: Specifies the expiration for the lifecycle of the object in the form of days. Eg: 30 (days)

        :type prefix: string
        :param prefix: location of the bucket

        :type noncurrent_days: int
        :param noncurrent_days: Specifies the number of days an object is noncurrent before Amazon S3 permanently deletes the noncurrent object versions.

        :rtype: Dict of the response of adding lifecycle configuration
    """
    s3Client = handle.client("s3", region_name=region)
    try:
        lifecycle_config = {
            'Rules': [
                {
                    'Expiration': {
                        'Days': expiration_days,
                    },
                    'Filter': {
                        'Prefix': ''
                    },
                    'Status': 'Enabled',
                    'NoncurrentVersionExpiration': {
                        'NoncurrentDays': noncurrent_days
                    }
                }
            ]
        }
        bucket_name = 'testrunbook'
        response = s3Client.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration=lifecycle_config
        )
    except Exception as e:
        raise e
    return response


