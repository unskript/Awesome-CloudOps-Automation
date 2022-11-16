##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import json
from builtins import int
from pydantic import BaseModel, Field
from typing import List, Dict
from subprocess import PIPE, run
import subprocess
import pprint


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
    query: str = Field(
        title='Query',
        description='Query string in compact Lucene query syntax. For eg: foo:bar'
    )
    index: str = Field(
        '',
        title='Index',
        description='A comma-separated list of index names to search; use _all or empty string to perform the operation on all indices.'
    )
    size: int = Field(
        '100',
        title='Number of hits to return.',
        description='The number of hits to return.'
    )
    sort: list = Field(
        None,
        title='List of fields to sort on.',
        description='Comma separated field names. For eg. [{"order_date":"desc"}, "order_id"]',
    )
    fields: List = Field(
        None,
        title='List of fields to return.',
        description='Comma separated list of fields to return. For eg. ["customer_name", "order_id"]'
    )


def elasticsearch_search_query_new_printer(output):
    if output is None:
        return
    for item in output:
        pprint.pprint(item)


def elasticsearch_search_query_new(handle,
                                   host: str,
                                   api_key: str,
                                   port: int,
                                   query: str = "",
                                   index: str = "",
                                   size: int = 100,
                                   fields: List = [],
                                   sort: List = []) -> List:
    """elasticsearch_search_query_new does an elasticsearch search on the provided query .
             :type handle: object
             :param handle: Object returned from Task Validate

             :type host: str
             :param host: URL of your Elasticsearch server

             :type port: int
<<<<<<< HEAD
             :param port: Port used by your Elasticsearch server
=======
             :param host: Port used by your Elasticsearch server
>>>>>>> master

             :type api_key: str
             :param api_key: API Key for authentication of the request

             :type query: str
             :param query: Query String

             :type index: str
             :param index: Index, Optional variable for the elasticsearch query

             :type size: int
             :param size: Size, Optional variable Size

             :type sort: List
             :param sort: Sort, Optional List

             :type fields: List
             :param fields: Fields, Optional List

             :rtype: Result List of Logs
     """
    es_path = host + ":" + str(port) + "/_search" + "?index=" + index + "&size=" + str(size) + "&pretty"
    es_header = "Authorization: ApiKey" + " " + api_key
    es_dict = {"query": {"query_string": {"query": query
        , "fields": fields
                                          }}, "sort": sort}
    es_json = json.dumps(es_dict)
    cmd = ["curl", "-k", "-XGET", "-H", "Content-Type: application/json", "-H",
           es_header,
           es_path,
           "-d",
           str(es_json)]
    try:
        raw_result = subprocess.check_output(cmd, stderr=PIPE, universal_newlines=True, shell=False)
        new_result = raw_result.replace("\n", "")
        result_dict = json.loads(new_result)
        print("Got %d Hits: " % result_dict['hits']['total']['value'])
        res = result_dict['hits']['hits']
        l = ["log"]
        result_list = []
        for each_label in res:
            for metadata in each_label:
                if metadata == "_source":
                    data_from_source = each_label[metadata]
                    for key in data_from_source:
                        if key in l:
                            result_list.append(data_from_source[key])
        print("Logs:")
        return result_list
    except subprocess.CalledProcessError as e:
        return e.output
