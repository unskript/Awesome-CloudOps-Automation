##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import json
from pydantic import BaseModel, Field
from typing import List, Dict


class InputSchema(BaseModel):
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
    fields: List[str] = Field(
        None,
        title='List of fields to return.',
        description='Comma separated list of fields to return. For eg. ["customer_name", "order_id"]'
    )

def elasticsearch_search_query_printer(output):
        for num,doc in enumerate(output):
            print(f'DOC ID: {doc["_id"]}')
            print(json.dumps(doc["_source"]))
    

def elasticsearch_search_query(handle, 
                               query: str, 
                               index: str = '', 
                               size: int = 100, 
                               sort: List = None,
                               fields: List = None) -> List:
    """elasticsearch_search Does an elasticsearch search on the provided query.

        :type handle: object
        :param handle: Object returned from Task Validate

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

        :rtype: Result Dictionary of result
    """
    # Input param validation.

    result = {}
    data = handle.search(query={"query_string": {"query": query}}, index=index, size=size, sort=sort, _source=fields)
    print("Got %d Hits: " % data['hits']['total']['value'])
    result = data['hits']['hits']

    return result
