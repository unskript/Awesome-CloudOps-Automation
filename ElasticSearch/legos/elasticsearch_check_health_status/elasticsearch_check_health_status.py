##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import subprocess
import pprint
from pydantic import BaseModel, Field
from typing import Dict
from subprocess import PIPE
import json


class InputSchema(BaseModel):
    pass

def elasticsearch_check_health_status_printer(output):
    if output is None:
        return
    print(output)


def elasticsearch_check_health_status(handle) -> Dict:
    """elasticsearch_check_health_status checks the status of an Elasticsearch cluster .

            :type handle: object
            :param handle: Object returned from Task Validate

            :rtype: Result Dict of result
    """
    
    output = handle.web_request("/_cluster/health?pretty",  # Path
                                "GET",                      # Method
                                None)                       # Data

    # es_path = host + ":"+str(port) + "/_cluster/health?pretty"
    # es_header = "Authorization: ApiKey" + " " + api_key
    # cmd = ["curl", "-k", "-XGET", "-H", es_header, es_path]
    # try:
    #     raw_result = subprocess.check_output(cmd, stderr=PIPE, universal_newlines=True, shell=False)
    #     new_result = raw_result.replace("\n", "")
    #     result_dict = json.loads(new_result)
    #     d = {}
    #     for key in result_dict:
    #         d[key] = result_dict[key]
    #     print("The status for " + d["cluster_name"] + " is " + d["status"])
    #     return d
    # except subprocess.CalledProcessError as e:
    #     return e.output

    return output.args