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
    checkid: int = Field(
        title='Check ID',
        description='Pingdom Check ID')
    status: Optional[str] = Field(
        'down',
        title="Status",
        description="Filter to only show specified results.Comma seperated string. example: down,unconfirmed,unknown")
    limit: Optional[int] = Field(
        10,
        title="Limit",
        description="Number of results to get")


def pingdom_get_results_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def pingdom_get_results(handle, checkid: int, status: str = 'down', limit: int = 10) -> Dict:
    """pingdom_get_result returns a lit of raw test results for a specified check
        
        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type checkid: int
        :param checkid: Pingdom Check ID.

        :type status: str
        :param status: Filter to only show specified results.Comma seperated string.

        :type limit: int
        :param limit: Number of returned checks.

        :rtype: Returns the raw results for a given checkID.
    """
    check = pingdom_client.ResultsApi(api_client=handle)
    result = check.results_checkid_get_with_http_info(_return_http_data_only=True, checkid=checkid, status=status,
                                                      limit=limit)
    return result
