##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field
import pymongo


class InputSchema(BaseModel):
    database_name: str = Field(
        title='Database Name',
        description='Name of the MongoDB database.'
    )
    collection_name: str = Field(
        title='Collection Name',
        description='Name of the MongoDB collection.'
    )
    documents: list = Field(
        title='Documents',
        description='''
            An array of documents to insert into the collection.
            For eg. Fo [ {"foo": "bar"} ... ]
            '''
    )


def mongodb_insert_document_printer(output):
    if output is None:
        return
    if isinstance(output, List):
        if len(output) == 0:
            print("No Documents Inserted.")
            return
        print(f"Inserted {len(output)} Documents with IDs: ")
        for entry in output:
            pprint.pprint(entry)


def mongodb_insert_document(
        handle,
        database_name: str,
        collection_name: str, 
        documents: list
        ) -> List:
    """mongodb_insert_document Runs mongo insert commands with the provided parameters.

        :type handle: object
        :param handle: Object returned from the Task Validate method

        :type database_name: str
        :param database_name: Name of the MongoDB database

        :type collection_name: str
        :param collection_name: Collection name in the MongoDB database

        :type document: list
        :param document: Document to be inserted in the MongoDB collection

        :rtype: List containing Insert IDs
    """
    # Input param validation.

    # Lets make sure the handle that is returned is not stale
    # and can connect to the MongoDB server
    try:
        handle.server_info()
    except (pymongo.errors.AutoReconnect, pymongo.errors.ServerSelectionTimeoutError) as e:
        print("[UNSKRIPT]: Reconnection / Server Selection Timeout Error: ", str(e))
        raise e
    except Exception as e:
        print("[UNSKRIPT]: Error Connecting: ", str(e))
        raise e



    try:
        db = handle[database_name]
        res = db[collection_name].insert_many(documents)
        return res.inserted_ids
    except Exception as e:
        print("[UNSKRIPT]: Error while Inserting Document(s): ", str(e))
        raise e
