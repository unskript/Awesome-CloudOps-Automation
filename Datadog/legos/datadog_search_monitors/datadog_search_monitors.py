##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List, Optional
from pydantic import BaseModel, Field
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client import ApiClient


class InputSchema(BaseModel):
    query: Optional[str] = Field(
        title='Query String',
        description='''After entering a search query in your `Manage Monitor page
        <https://app.datadoghq.com/monitors/manage>`_ use the query parameter value in the
        URL of the page as value for this parameter. Consult the dedicated `manage monitor
        documentation </monitors/manage/#find-the-monitors>`_ page to learn more. The query 
        can contain any number of space-separated monitor attributes, for instance 
        ``query="type:metric status:alert"``.''')
    name: Optional[str] = Field(
        title='Name',
        description='A string to filter monitors by name.')


def datadog_search_monitors_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def datadog_search_monitors(handle,
                            query: str = "",
                            name: str = "") -> List[dict]:
    """datadog_search_monitors searches monitors in datadog based on filters

        :type query: str
        :param query: After entering a search query in your `Manage Monitor page 
        <https://app.datadoghq.com/monitors/manage>`_ use the query parameter value in the
        URL of the page as value for this parameter. Consult the dedicated `manage monitor 
        documentation </monitors/manage/#find-the-monitors>`_ page to learn more. The query 
        can contain any number of space-separated monitor attributes, for instance 
        ``query="type:metric status:alert"``.

        :type name: str
        :param name: A string to filter monitors by name.

        :rtype: The list of monitors.
    """
    try:
        with ApiClient(handle.handle_v2) as api_client:
            api_instance = MonitorsApi(api_client)
            monitors = []
            page = 0
            if query != "":
                while True:
                    # The default page_size is 30
                    monitor_response = api_instance.search_monitors(page=page, query=query)
                    if page == monitor_response['metadata']['page_count']:
                        break
                    monitors.extend(monitor_response['monitors'])
                    page += 1
            else:
                while True:
                    response = api_instance.list_monitors(page_size=30,
                                                          page=page,
                                                          name=name)
                    if response == []:
                        break
                    monitors.extend(response)
                    page += 1
    except Exception as e:
        raise e
    return monitors
