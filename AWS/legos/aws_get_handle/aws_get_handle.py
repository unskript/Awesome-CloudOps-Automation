##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel
from unskript.connectors.aws import Session

class InputSchema(BaseModel):
    pass


def aws_get_handle(handle: Session):
    """aws_get_handle returns the AWS session handle.
       :rtype: AWS handle.
    """
    return handle