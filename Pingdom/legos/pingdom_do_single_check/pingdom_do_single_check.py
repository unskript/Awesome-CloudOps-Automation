##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from typing import Optional, Dict
from unskript.thirdparty.pingdom import swagger_client as pingdom_client

pp = pprint.PrettyPrinter(indent=4)

class InputSchema(BaseModel):
    host: str = Field(
        title='Host',
        description='Target Host')
    type: Optional[str] = Field(
        'http',
        title="Type",
        description='Target host type. Possible values: http, smtp, pop3, imap')


def pingdom_do_single_check_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def pingdom_do_single_check(handle, host: str, type: str = 'http') -> Dict:
    """pingdom_do_single_check performs a single test using a specified Pingdom probe against a specified target
        
        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type host: str
        :param host: Target Host.

        :type type: str
        :param type: Target host type.

        :rtype: Returns the results for a given single check.
    """
    # Input param validation.
    params = {}
    params['host'] = host
    params['type'] = type
    check = pingdom_client.SingleApi(api_client=handle)
    result = check.single_get(_return_http_data_only=True, host=host, type=type)
    return result
