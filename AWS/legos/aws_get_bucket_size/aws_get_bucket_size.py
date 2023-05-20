##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

import pprint
import datetime
from pydantic import BaseModel, Field
from boto3.session import Session


## FIXME: make this a JSON schema rather than class
class InputSchema(BaseModel):
    bucketName: str = Field(
        title='Bucket Name',
        description='Name of the bucket.')

def aws_get_bucket_size_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_bucket_size(handle: Session, bucketName: str) -> str:
    """aws_get_bucket_size Returns the size of the bucket.

        :type handle: Session
        :param handle: Handle to the boto3 session

        :type bucketName: string
        :param bucketName: Name of the bucket

        :rtype: String with the size of the bucket.
    """
    now = datetime.datetime.now()
    # Need to get the region of the bucket first.
    s3Client = handle.client('s3')
    try:
        bucketLocationResp = s3Client.get_bucket_location(
            Bucket=bucketName
        )
        print("location of bucket: ", bucketLocationResp)
    except Exception as e:
        print(f"Could not get location for bucket {bucketName}, error {e}")
        raise e
    region = bucketLocationResp['LocationConstraint']

    cw = handle.client('cloudwatch', region_name=region)

    # Gets the corresponding metrics from CloudWatch for bucket
    response = cw.get_metric_statistics(Namespace='AWS/S3',
                                        MetricName='BucketSizeBytes',
                                        Dimensions=[
                                            {'Name': 'BucketName', 'Value': bucketName},
                                            {'Name': 'StorageType', 'Value': 'StandardStorage'}
                                        ],
                                        Statistics=['Average'],
                                        Period=3600,
                                        StartTime=(now - datetime.timedelta(days=7)).isoformat(),
                                        EndTime=now.isoformat()
                                        )
    print(response)
    for res in response["Datapoints"]:
        return str(f"{int(res['Average'])}").rjust(25)
    # Note the use of "{:,}".format.
    # This is a new shorthand method to format output.
