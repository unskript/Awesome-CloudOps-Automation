##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import subprocess
import pprint
from pydantic import BaseModel, Field
from typing import List, Dict
from subprocess import PIPE, run
import json


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


def elasticsearch_enable_shard_allocation_printer(output):
    if output is None:
        return
    print("Shard allocations enabled for all kinds of shards")
    print(output)


def elasticsearch_enable_shard_allocation(handle,
                                           host: str,
                                           api_key: str,
                                           port: int) -> Dict:
    """elasticsearch_enable_shard_allocation enables shard allocations for any shards for any indices.

            :type handle: object
            :param handle: Object returned from Task Validate

            :type host: str
            :param host: URL of your Elasticsearch server

            :type port: int
            :param port: Port used by your Elasticsearch server

            :type api_key: str
            :param api_key: API Key for authentication of the request

            :rtype: Result Dict of result
    """
    es_path = host + ":" + str(port) + "/_cluster/settings?pretty"
    es_header = "Authorization: ApiKey" + " " + api_key
    es_dict = {"transient": {"cluster.routing.allocation.enable": "all"}}
    es_json = json.dumps(es_dict)
    cmd = ["curl", "-k", "-XPUT", "-H", "Content-Type: application/json", "-H",
           es_header,
           es_path,
           "-d",
           str(es_json)]
    try:
        raw_result = subprocess.check_output(cmd, stderr=PIPE, universal_newlines=True, shell=False)
        return raw_result
    except subprocess.CalledProcessError as e:
        return e.output
