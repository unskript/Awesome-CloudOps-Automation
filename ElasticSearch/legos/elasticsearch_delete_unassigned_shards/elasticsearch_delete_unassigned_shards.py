##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import subprocess
from pydantic import BaseModel, Field
from subprocess import PIPE, Popen


class InputSchema(BaseModel):
    pass


def elasticsearch_delete_unassigned_shards_printer(output):
    if output is None:
        return
    print(output)


def elasticsearch_delete_unassigned_shards(handle) -> str:
    """elasticsearch_delete_lost_shards deleted any corrupted/lost shards .

            :type handle: object
            :param handle: Object returned from Task Validate


            :rtype: Result String of result
    """
    output = handle.web_request("/_cat/shards?v=true&h=index,shard,prirep,state,node,unassigned.reason&s=state&pretty",  # Path
                            "GET",                      # Method
                            None)                       # Data
    list_of_shards = []
    for line in str(output.args).split('\n'):
        if "UNASSIGNED" in line:
            list_of_shards.append(line.split(" ")[0])

    if len(list_of_shards) != 0:
        output2 = handle.web_request("/" + list_of_shards, # Path
                                     "DELETE",  # Method
                                     None)      # Data

    o = output2.args
    if o == '':
        result = "No Unassigned shards found"
        return result
    result = "Successfully deleted unassigned shards"
    return result
