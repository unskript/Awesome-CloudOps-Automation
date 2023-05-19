##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from pydantic import BaseModel, Field
from unskript.enums.mongo_enums import UpdateCommands
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
    command: UpdateCommands = Field(
        UpdateCommands.update_one,
        title='Command',
        description='''
                         Db command
                         for Eg. update_one, update_many
                         Supported commands : update_one and update_many
                    '''
    )
    filter: dict = Field(
        title='Filter',
        description='A query that matches the document to update. For eg: {"foo":"bar"}.'
    )
    new_values: dict = Field(
        title='Update new fields to every document',
        description='''
                    The addition of fields apply in dictionary format.
                    For eg: { "$set": { "field": "value" } }
                    '''
    )
    upsert: bool = Field(
        True,
        title='Upsert',
        description='Allow creation of a new document, if one does not exist.'
    )


def mongodb_update_document_printer(output):
    if output is None:
        return
    print("\n")
    if output == 0:
        print("No Documents Updated")
    elif output > 1:
        print(f"Updated {output} Documents")
    else:
        print("Updated Given Document")


def mongodb_update_document(
        handle,
        database_name: str,
        collection_name: str,
        filter: dict,
        new_values: dict,
        command: UpdateCommands = UpdateCommands.update_one,
        upsert: bool = True) -> int:
    """mongodb_write_query Updates/creates an entry.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type database_name: str
        :param database_name: Name of the MongoDB database.

        :type collection_name: str
        :param collection_name: Name of the MongoDB collection.

        :type filter: Dict
        :param filter: A query that matches the document to update.

        :type new_values: Dict
        :param new_values: Update new fields to every document

        :type command: UpdateCommands
        :param command: Db command.
        
        :type upsert: bool
        :param upsert: Allow creation of a new document, if one does not exist.

        :rtype: int of updated document
    """
    # Input param validation.

    # Lets make sure the handle that is returned is not stale
    # and can connect to the MongoDB server
    try:
        handle.server_info()
    except (AutoReconnect, ServerSelectionTimeoutError) as e:
        print("[UNSKRIPT]: Reconnection / Server Selection Timeout Error: ", str(e))
        raise e
    except Exception as e:
        print("[UNSKRIPT]: Error Connecting: ", str(e))
        raise e

    try:
        record = None
        result = 0
        db = handle[database_name]

        if command == UpdateCommands.update_one:
            record = db[collection_name].update_one(filter, new_values, upsert=upsert)
        elif command == UpdateCommands.update_many:
            record = db[collection_name].update_many(
                filter, new_values, upsert=upsert)

        if record is not None:
            result = record.modified_count

        return result
    except Exception as e:
        raise e
