
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    region: str = Field(..., description='AWS region', title='region')
    service_code: str = Field(
        'ec2',
        description='The service code is used to get all quotas for the service',
        title='service_code',
    )

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
def aws_get_service_quotas_printer(output):
    if output is None:
        return
    pprint.pprint(output)
#list_service_quotas
#list_aws_default_service_quotas
@beartype
def aws_get_service_quotas(handle, service_code:str, region:str) -> List:
    sqClient = handle.client('service-quotas',region_name=region)
    resPaginate = aws_get_paginator(sqClient,'list_service_quotas','Quotas',
        ServiceCode=service_code,
        PaginationConfig={
            'MaxItems': 1000,
            'PageSize': 100
        })

    #res = sqClient.list_services(MaxResults = 100)
    return resPaginate


