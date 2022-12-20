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
    pass


def elasticsearch_disable_shard_allocation_printer(output):
    if output is None:
        return
    print("Shard allocations disabled for any kind shards")
    print(output)


def elasticsearch_disable_shard_allocation(handle) -> Dict:
    """elasticsearch_disable_shard_allocation disallows shard allocations for any indices.

            :type handle: object
            :param handle: Object returned from Task Validate

            :rtype: Result Dict of result
    """

    es_dict = {"transient": {"cluster.routing.allocation.enable": "none"}}
    output = handle.web_request("/_cluster/settings?pretty",  # Path
                                "PUT",                        # Method
                                es_dict)                      # Data

    # es_path = host + ":" + str(port) + "/_cluster/settings?pretty"
    # es_header = "Authorization: ApiKey" + " " + api_key
    # es_json = json.dumps(es_dict)
    # cmd = ["curl", "-k", "-XPUT", "-H", "Content-Type: application/json", "-H",
    #        es_header,
    #        es_path,
    #        "-d",
    #        str(es_json)]
    # try:
    #     raw_result = subprocess.check_output(cmd, stderr=PIPE, universal_newlines=True, shell=False)
    #     return raw_result
    # except subprocess.CalledProcessError as e:
    #     return e.output

    return output.args
