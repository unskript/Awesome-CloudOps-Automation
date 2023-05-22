##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from __future__ import annotations
import pprint
from typing import Dict
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def aws_describe_cloudtrail_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_describe_cloudtrail(handle, region:str) -> Dict:
    # Create a client object for CloudTrail
    cloudtrail_client = handle.client('cloudtrail', region_name=region)

    # Use the describe_trails method to get information about the available trails
    trails = cloudtrail_client.describe_trails()


    return trails
