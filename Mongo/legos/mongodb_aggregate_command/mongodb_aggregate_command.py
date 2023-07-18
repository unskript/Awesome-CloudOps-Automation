##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    database_name: str = Field(
        title='Database Name',
        description='Name of the MongoDB database'
    )
    collection_name: str = Field(
        title='Collection Name',
        description='Name of the MongoDB collection'
    )
    pipeline: list = Field(
        title='Pipeline',
        description='''
                A list of aggregation pipeline stages.
                For Eg. [  {
                            "$group" :
                                {"_id" : "$user", "num_tutorial" : {"$sum" : 1}}
                            }
                        ]
                In the above example, the documents are grouped on the basis of expression $user,
                and then the field num_tutorial includes the accumulator operator $sum that 
                calculates the number of tutorials of each user.
            '''
    )


def mongodb_aggregate_command_printer(output):
        print("\n\n")
        if isinstance(output, List):
            for entry in output:
                pprint.pprint(entry)
        else:
            pprint.pprint(output)


def mongodb_aggregate_command(
        handle,
        database_name: str,
        collection_name: str,
        pipeline: List
        ) -> List:
    """mongodb_aggregate_command Retrieves the documents present in the collection
    and the count of the documents using count_documents().

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type database_name: str
        :param database_name: Name of the MongoDB database.

        :type collection_name: str
        :param collection_name: Name of the MongoDB collection.

        :type pipeline: List
        :param pipeline: A list of aggregation pipeline stages.

        :rtype: List of All the results of the query.
    """

    try:
        result = []
        db = handle[database_name]
        res = db[collection_name].aggregate(pipeline=pipeline)
        for entry in res:
            result.append(entry)
        return result
    except Exception as e:
        return [e]
