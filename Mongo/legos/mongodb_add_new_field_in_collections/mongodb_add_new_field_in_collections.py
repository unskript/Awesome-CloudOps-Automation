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
    add_new_fields: dict = Field(
        title='Add new fields to every document',
        description='''
                The addition of fields apply in dictionary format.
                For eg: {"field":"value"}.
                '''
    )
    upsert: bool = Field(
        True,
        title='Upsert',
        description='Allow creation of a new document, if one does not exist.'
    )


def mongodb_add_new_field_in_collections_printer(output):
    if output is None:
        return
    print("\n\n")
    if isinstance(output, List):
        for entry in output:
            pprint.pprint(entry)
    else:
        pprint.pprint(output)


def mongodb_add_new_field_in_collections(handle, database_name: str, collection_name: str, add_new_fields: dict,
                                         upsert: bool = True) -> List:
    """mongodb_add_new_field_in_collections Add new field to every document in a MongoDB collection.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type database_name: str
        :param database_name: Name of the MongoDB database.

        :type collection_name: str
        :param collection_name: Name of the MongoDB collection.

        :type add_new_fields: Dict
        :param add_new_fields: Add new fields to every document.

        :type upsert: bool
        :param upsert: Allow creation of a new document, if one does not exist.

        :rtype: List with the objectID.
    """
    modifications = {"$set": add_new_fields}

    try:
        handle[database_name][collection_name].update_many(
            {},
            update=modifications,
            upsert=upsert)
        res = handle[database_name][collection_name].find()
        result = []
        for entry in res:
            result.append(entry)
        return result
    except Exception as e:
        return [e]
