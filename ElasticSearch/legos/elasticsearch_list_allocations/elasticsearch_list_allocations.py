##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import subprocess
from subprocess import PIPE
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    host: str = Field(
        title='Host',
        description='URL of Elasticsearch server'
    )
    port: int = Field(
        9200,
        title='Port',
        description='Port used by Elasticsearch'
    )
    api_key: str = Field(
        title='API Key',
        description='API Key for Authentication'
    )


def elasticsearch_list_allocations_printer(output):
    if output is None:
        return
    print(output)


def elasticsearch_list_allocations(handle,
                             host: str,
                             port: int,
                             api_key: str) -> str:
    """elasticsearch_list_allocations lists the allocations of an Elasticsearch cluster .

            :type handle: object
            :param handle: Object returned from Task Validate

            :type host: str
            :param host: URL of your Elasticsearch server

            :type port: int
            :param port: Port number at which Elasticsearch is listening

            :type api_key: str
            :param api_key: API Key for authentication of the request

            :rtype: Result String of result
    """

    es_path = host + ":" + str(port) + "/_cat/allocation?v=true&pretty"
    es_header = "Authorization: ApiKey" + " " + api_key
    cmd = ["curl", "-k", "-XGET", "-H", es_header, es_path]
    try:
        result = subprocess.check_output(cmd, stderr=PIPE, universal_newlines=True, shell=False)
        return result
    except subprocess.CalledProcessError as e:
        return e.output
