##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import Dict
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
    match_query: dict = Field(
        title='Match Query',
        description=('The selection criteria for the update in '
                     'dictionary format. For eg: {"foo":"bar"}.')
    )
    update: dict = Field(
        title='Update Document',
        description='''The modifications to apply in dictionary format.
        For eg: { "$set": { "field": "value" } }.'''
    )
    upsert: bool = Field(
        True,
        title='Upsert',
        description='Allow creation of a new document, if one does not exist.'
    )


def mongodb_write_query_printer(output):
    if output is None:
        return
    print("\n\n")
    if "error" in output:
        print(f'Error : {output["error"]}')
    print(
        f'MatchedCount: {output["matched_count"]}, ModifiedCount: {output["modified_count"]}')


def mongodb_write_query(
        handle,
        database_name: str,
        collection_name: str,
        match_query: dict,
        update: dict,
        upsert: bool = True
        ) -> Dict:
    """mongodb_write_query Updates/creates an entry.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type database_name: str
        :param database_name: Name of the MongoDB database.

        :type collection_name: str
        :param collection_name: Name of the MongoDB collection.

        :type match_query: Dict
        :param match_query: The selection criteria for the update in dictionary format.

        :type update: Dict
        :param update: The modifications to apply in dictionary format.

        :type upsert: bool
        :param upsert: Allow creation of a new document, if one does not exist.

        :rtype: Dict of Updated/created entry object.
    """
    # Input param validation.
    result = {}
    try:
        res = handle[database_name][collection_name].update_many(
            filter=match_query,
            update=update,
            upsert=upsert)
        result["matched_count"] = res.matched_count
        result["modified_count"] = res.modified_count
    except Exception as e:
        raise e
    # this is an object
    return result
