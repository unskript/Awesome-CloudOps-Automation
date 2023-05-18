##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from unskript.enums.mongo_enums import DeleteCommands
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
    command: DeleteCommands = Field(
        DeleteCommands.delete_one,
        title='Command Name',
        description='''
                         Name of command
                         for Eg. delete_one, delete_many
                         Supported commands : delete_one and delete_many
                    '''
    )
    filter: dict = Field(
        title='Filter Query',
        description='A query that matches the document to delete For eg: {"foo":"bar"}.'
    )

def mongodb_delete_document_printer(output):
    print("\n")
    if output == 0:
        print("No Documents were deleted")
    elif output > 1:
        print(f"{output.deleted_count} Documents Deleted")
    else:
        print("Document Deleted")



def mongodb_delete_document(
        handle,
        database_name: str,
        collection_name: str,
        command: DeleteCommands,
        filter: dict
        ) -> int:
    """mongodb_delete_document Runs mongo delete command with the provided parameters.

        :type handle: object
        :param handle: Handle returned from the Task validate command

        :type database_name: str
        :param database_name: Name of the MongoDB database

        :type collection_name: str
        :param collection_name: Name of the Collection to the delete the document from

        :type command: DeleteCommands
        :param command: Enum for DeleteCommand Options are delete_one or delete_many

        :type filter: dict
        :param filter: Search Filter to perform the delete operation on

        :rtype: Count of deleted document
    """
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
        result = None
        db = handle[database_name]
        if command == DeleteCommands.delete_one:
            result = db[collection_name].delete_one(filter)
            return result.deleted_count
        if command == DeleteCommands.delete_many:
            result = db[collection_name].delete_many(filter)
            return result.deleted_count
    except Exception as e:
        raise e
    return None
