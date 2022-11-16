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
    from_timestamp: Optional[int] = Field(
        0,
        title="Start Time",
        description='Timestamp in the UNIX Format date +%s')
    limit: Optional[int] = Field(
        100,
        title="Number of Results",
        description="Number of Results to Return")
    offset: Optional[int] = Field(
        0,
        title="Offset",
        description='Offset for Listing (requires limit to be specified)')
    to_timestamp: Optional[int] = Field(
        0,
        title="End Time",
        description='Timestamp in the UNIX Format date +%s')



def pingdom_get_analysis_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def pingdom_get_analysis(handle, checkid: int, from_timestamp: int = 0, limit: int = 100, offset: int = 0,
                         to_timestamp: int = 0) -> Dict:
    """pingdom_get_analysis returns the list of latest root cause analysis results for a specified check.
        
        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type checkid: int
        :param checkid: Pingdom Check ID.

        :type limit: int
        :param limit: Number of returned checks.

        :type  offset int
        :param offset: Offset of returned checks.

        :type from_timestamp: int
        :param from_timestamp: Start Time Timestamp in the UNIX Format date

        :type to_timestamp: int 
        :param to_timestamp: End Time Timestamp in the UNIX Format date

        :rtype: Returns the list of latest RCA results for a given check.
    """

    check = pingdom_client.AnalysisApi(api_client=handle)
    result = check.analysis_checkid_get_with_http_info(_return_http_data_only=True, checkid=checkid,
                                                       _from=from_timestamp if from_timestamp != 0 else None,
                                                       to=to_timestamp if to_timestamp != 0 else None, limit=limit,
                                                       offset=offset)
    return result
