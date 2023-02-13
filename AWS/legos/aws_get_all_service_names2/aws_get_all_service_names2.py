
from __future__ import annotations

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    region: str = Field(..., description='The AWS Regiob', title='region')

##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List, Dict
import pprint
from unskript.connectors.aws import aws_get_paginator

from beartype import beartype
@beartype
def aws_get_all_service_names2_printer(output):
    if output is None:
        return
    pprint.pprint(output)


@beartype
def aws_get_all_service_names2(handle, region:str) -> List:
    sqClient = handle.client('service-quotas',region_name=region)
    resPaginate = aws_get_paginator(sqClient,'list_services','Services',PaginationConfig={
        'MaxItems': 1000,
        'PageSize': 100
        })

    #res = sqClient.list_services(MaxResults = 100)
    return resPaginate


