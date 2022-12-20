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


def elasticsearch_delete_unassigned_shards(handle,
                                     host: str,
                                     port: int,
                                     api_key: str) -> str:
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
    # es_path = host + ":" + str(port) + "/_cat/shards?v=true&h=index,shard,prirep,state,node,unassigned.reason&s=state&pretty"
    # es_header = "Authorization: ApiKey" + " " + api_key
    # first_command = ["curl", "-k", "-XGET", "-H", es_header, es_path]
    # p1 = subprocess.Popen(first_command, shell=False, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    # second_command = ["grep", "UNASSIGNED"]
    # p2 = subprocess.Popen(second_command, stdin=p1.stdout, shell=False, stdout=PIPE, stderr=PIPE,
    #                       universal_newlines=True)
    # url = host + ":" + str(port) + "/{}"
    # third_command = ["awk", "{print $1}"]
    # p3 = subprocess.Popen(third_command, stdin=p2.stdout, stdout=PIPE, shell=False, universal_newlines=True)
    # var = p2.stdout.read()
    # fourth_command = ["xargs","-i", "curl" ,"-s", "-X", "DELETE",str(url)]
    # subprocess.Popen(fourth_command, stdin=p3.stdout, stdout=PIPE, shell=False, universal_newlines=True)
    if o == '':
        result = "No Unassigned shards found"
        return result
    result = "Successfully deleted unassigned shards"
    return result
