##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from unskript.thirdparty.pingdom import swagger_client as pingdom_client
import pprint

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    checkIds: Optional[List[str]] = Field(
        title='checkIds',
        description='List of check Ids to be modified. eg: ["1643815305","1643815323"].')
    pause: bool = Field(
        title="pause",
        description='True to pause the check Ids and false to unpause it.')
    resolution: int = Field(
        title="resolution",
        description='Interval time to test website (In Minutes). eg: 1 5 15 30 60.')


def pingdom_pause_or_unpause_checkids_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def pingdom_pause_or_unpause_checkids(handle, pause: bool, resolution: int, checkIds=None) -> Dict:
    """pingdom_pause_or_unpause_checkids returns the results pause or unpause check ids
        
        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type pause: bool
        :param pause: True to pause the check Ids and false to unpause it.

        :type resolution: int
        :param resolution: Interval time to test website (In Minutes). eg: 1 5 15 30 60.
        
        :type checkIds: List
        :param checkIds: List of check Ids to be modified.


        :rtype: Returns the list of result of all pause or unpause check ids
    """
    if checkIds is None:
        checkIds = []
    data = {"paused": pause, "resolution": resolution}
    if checkIds:
        data["checkids"] = ",".join(checkIds)
    check = pingdom_client.ChecksApi(api_client=handle)
    result = check.checks_put_with_http_info(body=data, _return_http_data_only=True)

    return result
