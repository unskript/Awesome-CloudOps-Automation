##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint
from datetime import datetime, timedelta
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def AWS_Start_IAM_Policy_Generation_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def AWS_Start_IAM_Policy_Generation(
        handle,
        region:str,
        CloudTrailARN:str,
        IAMPrincipalARN:str,
        AccessRole:str,
        hours:float
        ) -> str:

    client = handle.client('accessanalyzer', region_name=region)
    policyGenerationDict = {'principalArn': IAMPrincipalARN}
    myTrail = {'cloudTrailArn': CloudTrailARN,
                   'regions': [region],
                   'allRegions': False
              }
    endTime = datetime.now()
    endTime = endTime.strftime("%Y-%m-%dT%H:%M:%S")
    startTime = datetime.now()- timedelta(hours =hours)
    startTime =startTime.strftime("%Y-%m-%dT%H:%M:%S")
    response = client.start_policy_generation(
        policyGenerationDetails=policyGenerationDict,
        cloudTrailDetails={
            'trails': [myTrail],
            'accessRole': AccessRole,
            'startTime': startTime,
            'endTime': endTime
        }
    )
    jobId = response['jobId']
    return jobId
