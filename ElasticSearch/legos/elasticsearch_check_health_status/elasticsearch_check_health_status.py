##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import subprocess
import pprint
from pydantic import BaseModel, Field
from typing import Dict, Tuple
from subprocess import PIPE
import json


class InputSchema(BaseModel):
    pass

def elasticsearch_check_health_status_printer(output):
    if output is None:
        return
    print(output)


def elasticsearch_check_health_status(handle) -> Tuple:
    """elasticsearch_check_health_status checks the status of an Elasticsearch cluster .

            :type handle: object
            :param handle: Object returned from Task Validate

            :rtype: Result Dict of result
    """
    result = []
    cluster_health ={}
    output = handle.web_request("/_cluster/health?pretty",  # Path
                                "GET",                      # Method
                                None)                       # Data
    
    if output['status'] != 'green':
        cluster_health[output['cluster_name']] = output['status'] 
        result.append(cluster_health)
    if len(result) != 0:
        return(False, result)
    else:
        return(True, None)