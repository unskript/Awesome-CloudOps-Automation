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

         description='Id of Redshift Query', title='queryId'

    )
    

@beartype
def aws_get_redshift_query_details(handle, region: str, queryId:str) -> Dict:

    client = handle.client('redshift-data', region_name=region)
    response = client.describe_statement(
    Id=queryId
    )
    resultReady = response['HasResultSet']
    queryTimeNs = response['Duration']
    ResultRows = response['ResultRows']
    details = {"Status": response['Status'],
                "resultReady": resultReady, 
               "queryTimeNs":queryTimeNs,
               "ResultRows":ResultRows
              }
    return details


