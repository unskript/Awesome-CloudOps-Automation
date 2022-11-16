##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime as dt, timedelta
from unskript.thirdparty.pingdom import swagger_client as pingdom_client
import pprint

pp = pprint.PrettyPrinter(indent=4)

class InputSchema(BaseModel):
    description: str = Field(
        title='Description',
        description='Description for the maintenance window.')
    duration: int = Field(
        title='duration',
        description='Select a duration in minutes eg: 60.')
    tmsids: Optional[List[int]] = Field(
        default=None,
        title='Transaction checks Ids',
        description='Transaction checks Ids to assign to the maintenance window eg: [120824,1208233].')
    uptimeids: Optional[List[int]] = Field(
        default=None,
        title='Uptime Ids',
        description='Uptime checks Ids to assign to the maintenance window eg: [11061762,11061787].')


def pingdom_create_new_maintenance_window_printer(output):
    if output is None:
        return
    print("\n")
    pp.pprint(
        f'Successfully created maintenance window {output}, starting time {dt.now().strftime("%H:%M:%S")}')


def pingdom_create_new_maintenance_window(handle,
                                          description: str,
                                          duration: int,
                                          tmsids=None,
                                          uptimeids=None) -> int:
    """pingdom_create_new_maintenance_window .

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type description: str
        :param description: Description for the maintenance window.

        :type duration: int
        :param duration: Duration in minutes eg: 60.
        
        :type tmsids: list
        :param tmsids: Transaction checks Ids.

        :type uptimeids: list
        :param uptimeids: Uptime checks Ids to assign to the maintenance window.

        :rtype:success message with window id.
    """
    if uptimeids is None:
        uptimeids = []
    if tmsids is None:
        tmsids = []
    obj = {}
    obj['description'] = description
    start_time = dt.now()
    to_time = (start_time + timedelta(minutes=duration)).strftime("%s")

    obj['from'] = start_time.strftime("%s")
    obj['to'] = to_time

    if tmsids != None:
        obj['tmsids'] = tmsids

    if uptimeids != None:
        obj['uptimeids'] = uptimeids

    maintenance = pingdom_client.MaintenanceApi(api_client=handle)
    result = maintenance.maintenance_post_with_http_info(_return_http_data_only=True, body=obj)
    return result.maintenance.id
