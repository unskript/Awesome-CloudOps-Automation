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


def elasticsearch_check_health_status_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def elasticsearch_check_health_status(handle,
                                      host: str,
                                      port: int,
                                      api_key: str) -> Dict:
    """elasticsearch_check_health_status checks the status of an Elasticsearch cluster .

            :type handle: object
            :param handle: Object returned from Task Validate

            :type host: str
            :param host: URL of your Elasticsearch server

            :type port: int
            :param host: Port used by your Elasticsearch server

            :type api_key: str
            :param api_key: API Key for authentication of the request

            :rtype: Result Dict of result
    """
    es_path = host + ":"+str(port) + "/_cluster/health?pretty"
    es_header = "Authorization: ApiKey" + " " + api_key
    cmd = ["curl", "-k", "-XGET", "-H", es_header, es_path]
    try:
        raw_result = subprocess.check_output(cmd, stderr=PIPE, universal_newlines=True, shell=False)
        new_result = raw_result.replace("\n", "")
        result_dict = json.loads(new_result)
        d = {}
        for key in result_dict:
            d[key] = result_dict[key]
        print("The status for " + d["cluster_name"] + " is " + d["status"])
        return d
    except subprocess.CalledProcessError as e:
        return e.output
