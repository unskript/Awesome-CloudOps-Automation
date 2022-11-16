##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, List
from unskript.thirdparty.pingdom import swagger_client as pingdom_client
import pprint

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    host_name: Optional[str] = Field(
        default=None,
        title='Hostname',
        description='Name of the target host.')


def pingdom_get_checkids_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def pingdom_get_checkids(handle, host_name: str = "") -> List[str]:
    """pingdom_get_checkids.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type host_name: str
        :param host_name: Name of the target host.

        :rtype: list of checkids.
    """
    check = pingdom_client.ChecksApi(api_client=handle)
    result = check.checks_get_with_http_info(_return_http_data_only=True)
    res = result.checks
    if host_name:
        res = [check.id for check in res if check.hostname == host_name]
    else:
        res = [check.id for check in res]

    return res
