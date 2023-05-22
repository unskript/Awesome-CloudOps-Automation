##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel
from unskript.connectors.infra import InfraConnector

class InputSchema(BaseModel):
    pass


def infra_workflow_done(handle: InfraConnector):
    """infra_workflow_done stops workflow execution (Not implemented).
        :rtype: None.
    """
    return handle.done("Success")
