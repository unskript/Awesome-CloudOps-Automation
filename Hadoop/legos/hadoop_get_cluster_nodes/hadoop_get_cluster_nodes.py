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
        title='States',
        description=('The states of the node, specified as a comma-separated list, '
                     'valid values are: NEW, RUNNING, UNHEALTHY, DECOMMISSIONING, '
                     'DECOMMISSIONED, LOST, REBOOTED, SHUTDOWN')
    )


def hadoop_get_cluster_nodes_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def hadoop_get_cluster_nodes(handle, states: str = "") -> Dict:
    """hadoop_get_cluster_nodes get cluster nodes

        :type states: str
        :param states: The states of the node, specified as a comma-separated.

        :rtype: Dict cluster nodes
    """
    return handle.get_cluster_nodes(states=states if states else None)
