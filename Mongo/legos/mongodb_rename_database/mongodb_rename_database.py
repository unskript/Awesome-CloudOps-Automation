##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import os
import pprint
import bson
from typing import List
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    old_database_name: str = Field(
        title='Old Database Name',
        description='''
             Name of the MongoDB database that user want to change.
             Warning : This solution is not suitable for big or complex databases
            '''
    )
    new_database_name: str = Field(
        title='New Database Name',
        description='''
        New name of the MongoDB database.
        Warning : This solution is not suitable for big or complex databases
        '''
    )


def mongodb_rename_database_printer(output):
    if output is None:
        return
    print("\n\n")
    if isinstance(output, Exception):
        pprint.pprint("Error : {}".format(output))
    else:
        pprint.pprint("List of databases after renaming")
        pprint.pprint(output)


def mongodb_rename_database(handle, old_database_name: str, new_database_name: str) -> List:
    """mongodb_rename_database rename database in mongodb.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type old_database_name: str
        :param old_database_name: Name of the MongoDB database that user want to change.

        :type new_database_name: str
        :param new_database_name: New name of the MongoDB database.

        :rtype: All the results of the query.
    """

    def dump(collections, conn, db_name, path):
        """
        MongoDB Dump
        :param collections: Database collections name
        :param conn: MongoDB client connection
        :param db_name: Database name
        :param path:
        :return:
        """
        try:
            db = conn[db_name]
            for coll in collections:
                with open(os.path.join(path, f'{coll}.bson'), 'wb+') as f:
                    for doc in db[coll].find():
                        f.write(bson.BSON.encode(doc))
            return True
        except Exception as e:
            raise e

    def restore(path, conn, db_name):
        """
        MongoDB Restore
        :param path: Database dumped path
        :param conn: MongoDB client connection
        :param db_name: Database name
        :return:

        """
        try:
            db = conn[db_name]
            for coll in os.listdir(path):
                if coll.endswith('.bson'):
                    with open(os.path.join(path, coll), 'rb+') as f:
                        db[coll.split('.')[0]].insert_many(bson.decode_all(f.read()))
            return True
        except Exception as e:
            raise e
        finally:
            for coll in os.listdir(path):
                if coll.endswith('.bson'):
                    os.remove(os.path.join(path, coll))

    # Input param validation.

    try:
        db = handle[old_database_name]
        collection_list = db.list_collection_names()
        path = "/tmp/"
        # Steps 1 : Take a dump of old db
        is_backup = dump(collection_list, handle, old_database_name, path)
        # Step 2 : Restore the same dum in new db
        is_restore = False
        if is_backup:
            is_restore = restore(path, handle, new_database_name)
        # Step 3 : Drop the old Db
        if is_restore:
            handle.drop_database(old_database_name)

        # Verification
        dblist = handle.list_database_names()
        if new_database_name not in dblist:
            return [Exception("Error Occured !!!")]
        return dblist
    except Exception as e:
        return [e]
