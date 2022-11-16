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
        description='Name of the MongoDB database'
    )
    collection_name: str = Field(
        title='Collection Name',
        description='Name of the MongoDB collection'
    )



def mongodb_delete_collection_printer(output):
    if output is None:
        return
    print("\n\n")
    if isinstance(output, Exception):
        pprint.pprint("Error : {}".format(output))
        return output
    else:
        collections_before_drop = output[0]
        collections_after_drop = output[1]
        pprint.pprint("Collection count BEFORE drop:{}".format(len(collections_before_drop)))
        pprint.pprint("Collection count AFTER drop:{}".format(len(collections_after_drop)))
        diff = len(collections_before_drop) - len(collections_after_drop)
        if diff != 0:
            pprint.pprint("Collection deleted successfully !!!")


def mongodb_delete_collection(handle, database_name: str, collection_name: str) -> List:
    """mongodb_delete_collection delete collection from mongodb database.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type database_name: str
        :param database_name: Name of the MongoDB database.

        :type collection_name: str
        :param collection_name: Name of the MongoDB collection.

        :rtype: List of the results of the delete query.
    """
    # Input param validation.

    try:
        db = handle[database_name]

        collections_before_drop = db.list_collection_names()
        db.drop_collection(collection_name)
        # Verification
        collections_after_drop = db.list_collection_names()
        return [collections_before_drop, collections_after_drop]
    except Exception as e:
        return [e]
