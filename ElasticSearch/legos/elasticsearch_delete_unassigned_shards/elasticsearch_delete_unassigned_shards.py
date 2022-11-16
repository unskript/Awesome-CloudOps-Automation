##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import subprocess
from pydantic import BaseModel, Field
from subprocess import PIPE, Popen


class InputSchema(BaseModel):
    host: str = Field(
        title='Host',
        description='URL of Elasticsearch server'
    )
    port: int = Field(
        9200,
        title='Port',
        description='Port used by Elasticsearch.'
    )
    api_key: str = Field(
        title='API Key',
        description='API Key for Authentication'
    )


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

            :type host: str
            :param host: URL of your Elasticsearch server

            :type port: int
            :param port: Port used by your Elasticsearch server

            :type api_key: str
            :param api_key: API Key for authentication of the request

            :rtype: Result String of result
    """
    es_path = host + ":" + str(port) + "/_cat/shards?v=true&h=index,shard,prirep,state,node,unassigned.reason&s=state&pretty"
    es_header = "Authorization: ApiKey" + " " + api_key
    first_command = ["curl", "-k", "-XGET", "-H", es_header, es_path]
    p1 = subprocess.Popen(first_command, shell=False, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    second_command = ["grep", "UNASSIGNED"]
    p2 = subprocess.Popen(second_command, stdin=p1.stdout, shell=False, stdout=PIPE, stderr=PIPE,
                          universal_newlines=True)
    url = host + ":" + str(port) + "/{}"
    third_command = ["awk", "{print $1}"]
    p3 = subprocess.Popen(third_command, stdin=p2.stdout, stdout=PIPE, shell=False, universal_newlines=True)
    var = p2.stdout.read()
    fourth_command = ["xargs","-i", "curl" ,"-s", "-X", "DELETE",str(url)]
    subprocess.Popen(fourth_command, stdin=p3.stdout, stdout=PIPE, shell=False, universal_newlines=True)
    if var == '':
        result = "No Unassigned shards found"
        return result
    result = "Successfully deleted unassigned shards"
    return result
