##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def terraform_get_handle(handle):
    """
    terraform_get_handle returns the terraform handle.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :rtype: terraform handle.
    """
    return handle
