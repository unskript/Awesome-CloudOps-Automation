##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Optional, Dict

from pydantic import BaseModel, Field

pp = pprint.PrettyPrinter()


class InputSchema(BaseModel):
    states: Optional[str] = Field(
        title='states',
        description='The states of the node, specified as a comma-separated list, valid values are: NEW, RUNNING, UNHEALTHY, DECOMMISSIONING, DECOMMISSIONED, LOST, REBOOTED, SHUTDOWN'
    )
    applicationTypes: Optional[str] = Field(
        title='Application Types',
        description='Types of the applications, specified as a comma-separated list.'
    )


def hadoop_get_cluster_appstatistics_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def hadoop_get_cluster_appstatistics(handle, states: str = "", applicationTypes: str = "") -> Dict:
    """hadoop_get_cluster_appstatistics get cluster app statistics

        :type states: str
        :param states: The states of the node, specified as a comma-separated.

        :type applicationTypes: str
        :param applicationTypes: Types of the applications, specified as a comma-separated list.

        :rtype: Dict cluster app statistics
    """
    return handle.get_cluster_appstatistics(states=states if states else None,
                                            applicationTypes=applicationTypes if applicationTypes else None)
