from __future__ import annotations
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
from pydantic import BaseModel, Field
from typing import List, Dict
import pprint
from beartype import beartype


class InputSchema(BaseModel):
    region: str = Field(..., description='The AWS Regiob', title='region')


@beartype
def aws_get_all_service_names_printer(output):
    if output is None:
        return
    pprint.pprint(output)



@beartype
def aws_get_all_service_names(handle, region:str) -> List:
    sqClient = handle.client('service-quotas',region_name=region)
    resPaginate = aws_get_paginator(sqClient,'list_services','Services',PaginationConfig={
        'MaxItems': 1000,
        'PageSize': 100
        })

    #res = sqClient.list_services(MaxResults = 100)
    return resPaginate




