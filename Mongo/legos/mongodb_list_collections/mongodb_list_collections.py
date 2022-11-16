##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from pymongo.errors import InvalidName
from typing import List


class InputSchema(BaseModel):
    database_name: str = Field(
        title='Database Name',
        description='Name of the MongoDB database'
    )


def mongodb_list_collections_printer(output):
    if output is None:
        return
    print("\n\n")
    if isinstance(output, Exception):
        pprint.pprint(output._message)
    else:
        pprint.pprint("List of collections in DB")
        pprint.pprint(output)


def mongodb_list_collections(handle, database_name: str) -> List:
    """mongodb_list_collections Returns list of all collection in MongoDB

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type database_name: str
        :param database_name: Name of the MongoDB database.

        :rtype: All the results of the query.
    """
    # Input param validation.

    try:

        db = handle[database_name]
        collection_list = db.list_collection_names()
        return collection_list
    except InvalidName as e:
        return [e]
