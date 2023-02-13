
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    new_quota: Optional[float] = Field(
        '', description='The new quota value', title='new_quota'
    )
    quota_code: Optional[str] = Field(
        '', description='Quota Code that increase is requested for', title='quota_code'
    )
    region: str = Field(..., description='AWS Region.', title='Region')
    service_code: Optional[str] = Field(
        '"ec2"',
        description='Service Code whose quota you are requesting a change on.',
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
def aws_get_service_quotas(handle, service_code:str, quota_code:str, new_quota:float,region:str) -> Dict:
    sqClient = handle.client('service-quotas',region_name=region)
    res = sqClient.request_service_quota_increase(
        ServiceCode=service_code,
        QuotaCode=quota_code,

        DesiredValue=new_quota)

    #res = sqClient.list_services(MaxResults = 100)
    return res

