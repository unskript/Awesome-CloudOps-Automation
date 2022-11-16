##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from typing import List


class InputSchema(BaseModel):
    database_name: str = Field(
        title='Database Name',
        description='Name of the MongoDB database.'
    )
    collection_name: str = Field(
        title='Collection Name',
        description='Name of the MongoDB collection.'
    )
    remove_fields: dict = Field(
        title='Remove fields from every document',
        description='''
                The Removal of field apply in dictionary format.
                For eg: {"field":"value"}.
                '''
    )
    upsert: bool = Field(
        True,
        title='Upsert',
        description='Allow creation of a new document, if one does not exist.'
    )


def mongodb_remove_field_in_collections_printer(output):
    if output is None:
        return
    print("\n\n")
    if isinstance(output, Exception):
        pprint.pprint("Error : {}".format(output))
    else:
        for entry in output:
            pprint.pprint(entry)


def mongodb_remove_field_in_collections(handle, database_name: str, collection_name: str, remove_fields: dict,
                                        upsert: bool = True) -> List:
    """mongodb_remove_field_in_collections Remove field from every document in a MongoDB collection.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type database_name: str
        :param database_name: Name of the MongoDB database.

        :type collection_name: str
        :param collection_name: Name of the MongoDB collection.

        :type remove_fields: Dict
        :param remove_fields: Remove fields from every document.

        :type upsert: bool
        :param upsert: Allow creation of a new document, if one does not exist.

        :rtype: string with the objectID.
    """
    # Input param validation.

    modifications = {"$unset": remove_fields}

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
