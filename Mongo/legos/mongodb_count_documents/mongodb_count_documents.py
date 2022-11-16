##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint

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
    filter: dict = Field(
        title='Filter Query',
        description='''
             A query document that selects which documents to count in the collection.
             Can be an empty document to count all documents.
             For eg: {"foo":"bar"}.
            '''
    )


def mongodb_count_documents_printer(output):
    if output is None:
        return
    if isinstance(output, int):
        pprint.pprint("Total number of documents : {}".format(output))
    else:
        pprint.pprint(output)


def mongodb_count_documents(handle, database_name: str, collection_name: str, filter: dict):
    """mongodb_count_documents Retrieves the documents present in the collection and the count of the documents using count_documents().

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type database_name: str
        :param database_name: Name of the MongoDB database.

        :type filter: Dict
        :param filter: A query that matches the document to filter.

        :rtype: All the results of the query.
    """
    # Input param validation.

    try:
        db = handle[database_name]
        total_count = db[collection_name].count_documents(filter)
        return total_count
    except Exception as e:
        return e
