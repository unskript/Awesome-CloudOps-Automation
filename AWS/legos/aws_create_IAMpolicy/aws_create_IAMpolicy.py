##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field, SecretStr
from typing import Dict, List
import pprint


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

