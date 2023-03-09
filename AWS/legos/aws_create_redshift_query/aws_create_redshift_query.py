##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##


from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Dict
from unskript.connectors.aws import aws_get_paginator
import pprint
from beartype import beartype


class InputSchema(BaseModel):
    region: str = Field(..., description='AWS Region.', title='Region')
    query: str = Field(
        '',
        description='sql query to run',
        title='query',
    )
    cluster: str = Field(
        '', description='Name of Redshift Cluster', title='cluster'
    )
    database: str = Field(
        '', description='Name of your Redshift database', title='database'
    )
    secretArn: str = Field(
        '', description='Value of your Secrets Manager ARN', title='secretArn'
    )




@beartype
def aws_create_redshift_query(handle, region: str,cluster:str, database:str, secretArn: str, query:str) -> str:

    # Input param validation.
    #major change
    client = handle.client('redshift-data', region_name=region)
    # define your query
    query = query
    #query = "SELECT * FROM PG_TABLE_DEF;"
    # execute the query
    response = client.execute_statement(
        ClusterIdentifier=cluster,
        Database=database,
        SecretArn=secretArn,
        Sql=query
    )
    resultId = response['Id']
    print(response)
    print("resultId",resultId)


    return resultId

#make a change
