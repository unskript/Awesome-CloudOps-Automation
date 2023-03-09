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



class InputSchema(BaseModel):
    resultId: str = Field(
        '', description='Redshift Query Result', title='resultId'
    )
    region: str = Field(..., description='AWS Region', title='region')




@beartype
def aws_get_redshift_result(handle, region:str, resultId: str) -> List:


    client = handle.client('redshift-data', region_name=region)
    result = client.get_statement_result(
        Id=resultId
    )
    #result has the Dictionary, but it is not easily queried
    #get all the columns into an array
    columnNames = []
    for column in result['ColumnMetadata']:
        columnNames.append(column['label'])
    #print(columnNames)

    #now let's make the output into a dict
    listResult = []
    for record in result['Records']:

        for key, value in record[0].items():
            rowId = value
        entryCounter = 0
        entryDict = {}
        for entry in record:

            for key, value in entry.items():
                entryDict[columnNames[entryCounter]] = value
            entryCounter +=1
        #print("entryDict",entryDict)
        listResult.append(entryDict)

    print(listResult)
    return listResult



