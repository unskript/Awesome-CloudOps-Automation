##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Dict
from unskript.thirdparty.pingdom import swagger_client as pingdom_client
import pprint

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    host: str = Field(
        title='Host',
        description='Target Host eg: google.com')
    probeid: Optional[int] = Field(
        title="Probe ID",
        description='Probe Identifier')


def pingdom_traceroute_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def pingdom_traceroute(handle, host: str, probeid = None) -> Dict:
    """pingdom_traceroute performs traceroute for a given host and returns result.
        
        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type host: str
        :param host: Target Host eg: google.com.

        :type probeid: str
        :param probeid: Probe Identifier.

        :rtype: Returns the list of latest RCA results for a given check.
    """


    traceroute = pingdom_client.TracerouteApi(api_client=handle)
    result = traceroute.traceroute_get_with_http_info(_return_http_data_only=True, host=host,
                                                      probeid=probeid if probeid != probeid else probeid)

    return result
