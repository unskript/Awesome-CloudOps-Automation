
from __future__ import annotations

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    region: str = Field(..., description='The AWS Regiob', title='region')

from unskript.connectors.aws import aws_get_paginator
from pydantic import BaseModel, Field
from typing import List, Dict

from beartype import beartype
@beartype
@beartype
def aws_get_all_service_names3_printer(output):
    if output is None:
        return
    pprint.pprint(output)


@beartype
@beartype
def aws_get_all_service_names3(handle, region:str) -> List:
    sqClient = handle.client('service-quotas',region_name=region)
    resPaginate = aws_get_paginator(sqClient,'list_services','Services',PaginationConfig={
        'MaxItems': 1000,
        'PageSize': 100
        })

    #res = sqClient.list_services(MaxResults = 100)
    return resPaginate




