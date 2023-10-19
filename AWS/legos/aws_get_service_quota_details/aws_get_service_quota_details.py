##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from __future__ import annotations
import pprint
from typing import Dict
from pydantic import BaseModel, Field
from beartype import beartype


class InputSchema(BaseModel):
    quota_code: str = Field(
        description='The quota code for the Service Type',
        title='quota_code',
    )
    region: str = Field(..., description='AWS Region.', title='Region')
    service_code: str = Field(
         description='The service code to be queried', title='service_code'
    )

@beartype
def aws_get_service_quota_details_printer(output):
    if output is None:
        return
    pprint.pprint(output)
#list_service_quotas
#list_aws_default_service_quotas
@beartype
def aws_get_service_quota_details(handle, service_code:str, quota_code:str, region:str) -> Dict:
    sqClient = handle.client('service-quotas',region_name=region)
    res = sqClient.get_service_quota(
        ServiceCode=service_code,
        QuotaCode=quota_code)

    #res = sqClient.list_services(MaxResults = 100)
    return res
