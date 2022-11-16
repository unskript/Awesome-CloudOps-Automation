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
    extended_tags: Optional[bool] = Field(
        False,
        title='Include Extended Tags',
        description='Include extended tags')
    limit: Optional[str] = Field(
        '100',
        title="Number of Checks",
        description='Number of returned checks')
    offset: Optional[str] = Field(
        '0',
        title="Offset",
        description="Offset of returned checks")
    tags: Optional[str] = Field(
        title="Tags",
        description='List of tags seperated by comma eg: nginx')
    type: Optional[str] = Field(
        title="Type",
        description='Filter Type: Possible values: script, recording')


def pingdom_get_tmschecke_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def pingdom_get_tmscheck(handle, extended_tags: bool = False, limit: int = 100, offset: int = 0, tags: str = "",
                         type: str = "") -> Dict:
    """pingdom_get_tmscheck returns the results of Transaction check

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type extended_tags: bool
        :param extended_tags: Include Extended Tags or Not.

        :type limit: int
        :param limit: Number of returned checks.

        :type  offset int
        :param offset: Offset of returned checks.

        :type tags: List
        :param tags:List of tags seperated by comma

        :type type: str
        :param type: Filter Type: Possible values: script, recording.

        :rtype: Returns the list of result of all transaction checks
    """

    check = pingdom_client.TMSChecksApi(api_client=handle)
    result = check.get_all_checks_with_http_info(_return_http_data_only=True, extended_tags=extended_tags, limit=limit,
                                                 offset=offset, tags=tags if tags != None else None, type=type)
    return result
