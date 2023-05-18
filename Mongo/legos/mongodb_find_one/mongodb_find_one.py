##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List, Optional
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
        description='A query that matches the document to find. For eg: { "name": "mike" }.'
    )
    projection: Optional[dict] = Field(
        default=None,
        title='Projection',
        description='''
                A list of field names that should be
                returned in the result document or a mapping specifying the fields
                to include or exclude. If `projection` is a list "_id" will
                always be returned. Use a mapping to exclude fields from
                the result (e.g. {'_id': false})
                ''')
    sort: Optional[list] = Field(
        default=None,
        title='Sort',
        description='''
                a list of {key:direction} pairs
                specifying the sort order for the query. If multiple documents
                match the query, they are sorted and the first is updated.
                (e.g. [{'age': '-1'}])
                '''
    )


def mongodb_find_one_printer(func):
    def Printer(*args, **kwargs):
        output = func(*args, **kwargs)
        print("\n\n")
        pprint.pprint(output)
        return output
    return Printer


@mongodb_find_one_printer
def mongodb_find_one(
        handle,
        database_name: str,
        collection_name: str,
        filter: dict,
        projection: dict = None,
        sort: List = None) -> dict:
    """mongodb_find_one and returns .

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type database_name: str
        :param database_name: Name of the MongoDB database.

        :type collection_name: str
        :param collection_name: Name of the MongoDB collection.

        :type match_query: Dict
        :param match_query: The selection criteria for the update in dictionary format.

        :type filter: Dict
        :param filter: A query that matches the document to find.

        :type projection: Dict
        :param projection: A list of field names that should be returned/excluded in the result.

        :type sort: list
        :param sort: A list of {key:direction} pairs.

        :rtype: Dict of matched query result.
    """
    try:
        db = handle[database_name]
        r = db[collection_name].find_one(
            filter, projection=projection, sort=sort if sort else None)
        return r or {}

    except Exception as e:
        return {"error" : str(e)}
