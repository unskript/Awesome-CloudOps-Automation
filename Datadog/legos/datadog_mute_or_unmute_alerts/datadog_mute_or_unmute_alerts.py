##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from ast import Str
from pydantic import BaseModel, Field
from typing import Optional, List
import pprint

class InputSchema(BaseModel):
    monitorIDs: Optional[List[int]] = Field(
        title='Monitor IDs',
        description='List of monitor Ids to be modified. eg: [1643815305,1643815323].')
    all: Optional[bool] = Field(
        title="All monitors",
        description='Set this to True if mute/unmute all monitors.')
    mute: bool = Field(
        True,
        title="Mute",
        description='True to mute, False to unmute.')
    scope: Optional[str] = Field(
        default=None,
        title="Scope",
        description='''
        The scope to apply the mute to. For example, if your alert is grouped by "host", you might mute "host:app1".
        ''')


def datadog_mute_or_unmute_alerts_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def datadog_mute_or_unmute_alerts(handle,
                                  monitorIDs: List[int] = [],
                                  all: bool = False,
                                  mute: bool = True,
                                  scope: str = "") -> Str:
    """datadog_mute_or_unmute_alerts mutes and unmutes alerts.

        :type monitorIDs: list
        :param monitorIDs: List of monitor Ids to be modified. eg: [1643815305,1643815323].
        
        :type all: bool
        :param all: Set this to True if mute/unmute all monitors.

        :type mute: bool
        :param mute: True to mute, False to unmute.
        
        :type scope: str    
        :param scope: The scope to apply the mute to. For example, if your alert is grouped by "host", you might mute "host:app1".

        :rtype: String with the execution status.
    """

    if mute:
        if all:
            if scope:
                handle.Monitor.mute_all(scope=scope)
            else:
                handle.Monitor.mute_all()
            return 'Successfully muted all monitors.'
        else:
            if scope:
                res = [handle.Monitor.mute(id=x, scope=scope) for x in monitorIDs]
            else:
                res = [handle.Monitor.mute(id=x) for x in monitorIDs]
            return 'Successfully muted monitors.'
    else:
        if all:
            if scope:
                handle.Monitor.unmute_all(scope=scope)
            else:
                handle.Monitor.unmute_all()
            return 'Successfully unmuted all monitors.'
        else:
            if scope:
                res = [handle.Monitor.unmute(id=x,scope=scope) for x in monitorIDs]
            else:
                res = [handle.Monitor.unmute(id=x) for x in monitorIDs]
        return 'Successfully umuted monitors.'
