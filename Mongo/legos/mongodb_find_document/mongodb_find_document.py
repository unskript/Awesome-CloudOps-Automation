##
# Copyright (c) 2022 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List, Optional
from pydantic import BaseModel, Field
from unskript.enums.mongo_enums import FindCommands
from pymongo import ReturnDocument
from pymongo.errors import AutoReconnect, ServerSelectionTimeoutError

class InputSchema(BaseModel):
    database_name: str = Field(
        title='Database Name',
        description='Name of the MongoDB database.'
    )
    collection_name: str = Field(
        title='Collection Name',
        description='Name of the MongoDB collection.'
    )
    command: Optional[FindCommands] = Field(
        default=FindCommands.find,
        title='Command',
        description='''
                        Name of command
                        for Eg. find,  etc
                        Supported commands : find, find_one_and_delete, find_one_and_replace, find_one_and_update
                '''
    )
    filter: dict = Field(
        title='Filter',
        description=('A query that matches the document to update, delete, find '
                     'and replace. For eg: {"foo":"bar"}.')
    )
    document: Optional[dict] = Field(
        default=None,
        title='Update/Replace Document',
        description='''
            The modifications to apply in dictionary format.
            For eg: For update : {"$set":{"field":"value"}} to Replace : {"field":"value"}
            Not applicable for find, find_one and find_one_and_delete
        '''
    )
    projection: Optional[dict] = Field(
        default=None,
        title='Projection ',
        description='''
                A list of field names that should be
                returned in the result document or a mapping specifying the fields
                to include or exclude. If `projection` is a list "_id" will
                always be returned. Use a mapping to exclude fields from
                the result (e.g. {'_id': False})
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

def mongodb_find_document_printer(output):
    if isinstance(output, List):
        if len(output) == 0:
            print("No Matching Documents.")
            return
        for entry in output:
            pprint.pprint(entry)


def mongodb_find_document(
        handle,
        database_name: str,
        collection_name: str,
        filter: dict,
        command: FindCommands = FindCommands.find,
        document: dict = None,
        projection: dict = None,
        sort: List = None) -> List:
    """mongodb_find_document Runs mongo find commands with the provided parameters.

        :type handle: object
        :param handle: Object returned from Task validate method

        :type database_name: str
        :param database_name: Name of the MongoDB database

        :type collection_name: str
        :param collection_name: Name of the MongoDB Collection to work on

        :type filter: dict
        :param filter: Filter in the dictionary form to work with

        :type command: FindCommands
        :param command: FindCommands Enum

        :type document: dict
        :param document: Document in the Dictionary form

        :type projection: dict
        :param projection: Projection in Dictionary form

        :type sort: List
        :param sort: Sort List to be used

        :rtype: All the results of the query.
    """

    # Lets make sure the handle that is returned is not stale
    # and can connect to the MongoDB server
    try:
        handle.server_info()
    except (AutoReconnect, ServerSelectionTimeoutError) as e:
        print(f"[UNSKRIPT]: Reconnection / Server Selection Timeout Error: {str(e)}")
        raise e
    except Exception as e:
        print(f"[UNSKRIPT]: Error Connecting: {str(e)}")
        raise e

    sort_by = sort
    update = document
    sort = []
    if sort_by:
        for val in sort_by:
            for k, v in val.items():
                sort.append((k, v))

    result = []
    try:
        db = handle[database_name]
        if command == FindCommands.find:
            records = db[collection_name].find(
                filter, projection=projection, sort=sort)
            for record in records:
                result.append(record)
        elif command == FindCommands.find_one:
            record = db[collection_name].find_one(
                filter, projection=projection, sort=sort)
            result.append(record)
        elif command == FindCommands.find_one_and_delete:
            record = db[collection_name].find_one_and_delete(
                filter, projection=projection, sort=sort)
            pprint.pprint("One matching document deleted")
            result.append(record)
        elif command == FindCommands.find_one_and_replace:
            record = db[collection_name].find_one_and_replace(
                filter, replacement=update, projection=projection,
                sort=sort, return_document=ReturnDocument.AFTER)
            pprint.pprint("One matching docuemnt replaced")
            result.append(record)
        elif command == FindCommands.find_one_and_update:
            record = db[collection_name].find_one_and_update(
                filter,
                update=update,
                projection=projection,
                sort=sort,
                return_document=ReturnDocument.AFTER
                )
            pprint.pprint("Document Updated")
            result.append(record)
        return result
    except Exception as e:
        raise e
