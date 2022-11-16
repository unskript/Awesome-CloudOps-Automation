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
        description='Name of the MongoDB database'
    )
    collection_name: str = Field(
        title='Collection Name',
        description='Name of the MongoDB collection'
    )
    key: str = Field(
        title='Name of field',
        description='''
                Name of the field for which we want to get the distinct values
            '''
    )
    filter: dict = Field(
        None,
        title='Filter Query',
        description='''
                A query document that specifies the documents from which to retrieve the distinct values.
                For eg: {"foo":"bar"}.
            '''
    )


def mongodb_distinct_command_printer(output):
    if output is None:
        return
    print("\n\n")
    if isinstance(output, List):
        for entry in output:
            pprint.pprint(entry)
    else:
        pprint.pprint(output)


def mongodb_distinct_command(handle, database_name: str, collection_name: str, key: str, filter=None) -> List:
    """mongodb_distinct_command Retrieves the documents present in the collection and the count of the documents using count_documents().

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type database_name: str
        :param database_name: Name of the MongoDB database.

        :type collection_name: str
        :param collection_name: Name of the MongoDB collection.

        :type key: str
        :param key: Name of the field for which we want to get the distinct values.

        :type filter Dict
        :param filter: A query that matches the document to filter.

        :rtype: All the results of the query.
    """
    # Input param validation.

    if filter is None:
        filter = {}
    try:
        result = []
        db = handle[database_name]
        res = db[collection_name].distinct(key, filter)
        for entry in res:
            result.append(entry)
        return result
    except Exception as e:
        return [e]
