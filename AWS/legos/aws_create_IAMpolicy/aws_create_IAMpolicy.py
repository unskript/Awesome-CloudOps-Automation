##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def aws_create_IAMpolicy_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_create_IAMpolicy(handle, policyDocument:str, PolicyName:str) -> Dict:

    client = handle.client('iam')
    response = client.create_policy(
        PolicyName=PolicyName,
        PolicyDocument=policyDocument,
        Description='generated Via unSkript',

    )
    return response
