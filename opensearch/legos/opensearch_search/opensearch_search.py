##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    query: dict = Field(
        title='Query',
        description='''
        Opensearch Query DSL. For eg. {
            "multi_match": {
              "query": "alice",
              "fields": ["title^2", "director"]
            }
          }
        '''
    )
    index: str = Field(
        '',
        title='Index',
        description=('A comma-separated list of index names to search; '
                     'use _all or empty string to perform the operation on all indices.')
    )
    size: int = Field(
        '100',
        title='Number of hits to return.',
        description='The number of hits to return.'
    )


def opensearch_search_printer(output):
    print('\n\n')
    all_hits = output['hits']['hits']
    print(f"Got {output['hits']['total']['value']} Hits:")

    for num, doc in enumerate(all_hits):
        pp.pprint(f'DOC ID: {doc["_id"]}')
        pp.pprint(doc["_source"])


def opensearch_search(handle, query: dict, index: str = '', size: int = 100) -> Dict:
    """opensearch_search Does an opensearch search on the provided query.

        :type query: dict
        :param query: Opensearch Query DSL.

        :type index: string
        :param index: A comma-separated list of index names to search;
        use _all or empty string to perform the operation on all indices.

        :type size: int
        :param size: The number of hits to return.

        :rtype: All the results of the query.
    """
    # Input param validation.

    if index:
        res = handle.search(body={"query": query}, index=index, size=size)
    else:
        res = handle.search(body={"query": query}, size=size)
    return res
