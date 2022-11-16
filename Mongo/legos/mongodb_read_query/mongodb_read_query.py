##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    database_name: str = Field(
        title='Database Name',
        description='Name of the MongoDB database.'
    )
    collection_name: str = Field(
        title='Collection Name',
        description='Name of the MongoDB collection.'
    )
    query: dict = Field(
        title='Read Query',
        description='Read only query in dictionary format. For eg: {"foo":"bar"}.'
    )

def mongodb_read_query_printer(output):
    if output is None:
        return
    print("\n\n")
    for entry in output:
        pprint.pprint(entry)


def mongodb_read_query(handle, database_name: str, collection_name: str, query: dict) -> List:
    """mongodb_read_query Runs mongo query with the provided parameters.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type database_name: str
        :param database_name: Name of the MongoDB database.

        :type collection_name: str
        :param collection_name: Name of the MongoDB collection.

        :type query: Dict
        :param query: Read only query in dictionary format.

        :rtype: All the results of the query.
    """
    try:
        res = handle[database_name][collection_name].find(query)
    except Exception as e:
        return [e]
    result = []
    for entry in res:
        result.append(entry)
    return result
