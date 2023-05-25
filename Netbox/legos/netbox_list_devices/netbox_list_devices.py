##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from pydantic import BaseModel

class InputSchema(BaseModel):
    pass

def netbox_list_devices_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def netbox_list_devices(handle):
    """netbox_list_devices returns the Netbox devices.

        :type handle: object
        :param handle: Object returned from task.validate(...).

          :rtype: List of netbox devices.
    """
    result = handle.dcim.devices.all()
    return result
