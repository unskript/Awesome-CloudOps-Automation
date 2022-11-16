#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def zabbix_get_handle(handle):
    """zabbix_get_handle returns the Zabbix handle.

        :type handle: object
        :param handle: Object returned from task.validate(...).


       :rtype: Zabbix Handle
    """
    return handle
