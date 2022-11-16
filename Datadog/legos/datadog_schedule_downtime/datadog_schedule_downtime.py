##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from ast import Str
from datetime import datetime as dt, timedelta
from typing import Optional, List, Any

from pydantic import BaseModel, Field
import pprint

class InputSchema(BaseModel):
    duration: int = Field(
        title='Duration',
        description='Select a duration in minutes eg: 60.'
    )
    scope: List[str] = Field(
        default='',
        title='Scope',
        description='The scope(s) to which the downtime applies.')
    monitor_id: Optional[int] = Field(
        default=None,
        title='Monitor Id',
        description='A single monitor to which the downtime applies. If not provided, the downtime applies to all monitors.')
    monitor_tags: Optional[List[str]] = Field(default=None,
                                              title='Monitor Tags',
                                              description='A comma-separated list of monitor tags')




def datadog_schedule_downtime_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def datadog_schedule_downtime(handle,
                              duration: int,
                              scope:list = [],
                              monitor_id: int = 0,
                              monitor_tags:list = []) -> Str:
    """datadog_schedule_downtime schedules a monitor downtime.

        :type duration: int
        :param duration: Select a duration in minutes eg: 60.
        
        :type scope: List
        :param scope: The scope(s) to which the downtime applies.

        :type monitor_id: int
        :param monitor_id: A single monitor to which the downtime applies. If not provided, the downtime applies to all monitors.
        
        :type monitor_tags: List
        :param monitor_tags: A comma-separated list of monitor tags.

        :rtype: String with the execution status.
    """
    start_time = dt.now()
    end_time = (start_time + timedelta(minutes=duration)).strftime("%s")
    try:
        res = handle.Downtime.create(scope=scope, start=start_time.strftime("%s"), end=end_time, monitor_id=monitor_id,
                                     monitor_tags=monitor_tags)
    except Exception as e:
        return 'Failed to schedule downtime, {}'.format(e)
    return 'Successfully scheduled downtime, ID {}, starting time {}'.format(res.get("id"), start_time.strftime("%H:%M:%S"))
