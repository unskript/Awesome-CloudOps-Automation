from __future__ import annotations
##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List, Dict
from unskript.connectors.aws import aws_get_paginator
import pprint
from beartype import beartype


from typing import Optional

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    region: str = Field(..., description='AWS Region.', title='Region')
    queryId: str = Field(
        '', description='Id of Redshift Query', title='queryId'
    )

@beartype
def aws_get_redshift_query_details(handle, region: str, queryId:str) -> Dict:

    client = handle.client('redshift-data', region_name=region)
    #result = aws_get_paginator(client, 
    #                           "get_statement_result", 
     #                           "TotalNumRows", 
     #                           Id='d7bda35c-7aa4-4414-9272-9e268320df40')
    response = client.describe_statement(
    Id=queryId
    )
    return response


