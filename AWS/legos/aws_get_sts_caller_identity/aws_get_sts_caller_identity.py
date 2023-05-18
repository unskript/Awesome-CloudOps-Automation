##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass

def aws_get_sts_caller_identity_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_sts_caller_identity(handle) -> Dict:
    """aws_get_caller_identity Returns an dict of STS caller identity info.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :rtype: dict of STS caller identity info
    """
    ec2Client = handle.client('sts')
    response = ec2Client.get_caller_identity()

    return response
