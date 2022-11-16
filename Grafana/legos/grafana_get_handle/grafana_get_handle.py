##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel

from unskript.connectors.grafana import Grafana


class InputSchema(BaseModel):
    pass


def grafana_get_handle(handle: Grafana) -> Grafana:
    """grafana_get_handle returns the grafana REST API handle.

       :rtype: grafana Handle.
    """
    return handle
