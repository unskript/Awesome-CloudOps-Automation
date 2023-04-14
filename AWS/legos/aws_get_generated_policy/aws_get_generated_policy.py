##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from __future__ import annotations
from pydantic import BaseModel, Field, SecretStr
from typing import Dict, List
import pprint




from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def aws_get_generated_policy_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_get_generated_policy(handle, region:str,jobId:str) -> Dict:
    client = handle.client('accessanalyzer', region_name=region)
    response = client.get_generated_policy(
        jobId=jobId,
        includeResourcePlaceholders=True,
        includeServiceLevelTemplate=True
    )
    return response

