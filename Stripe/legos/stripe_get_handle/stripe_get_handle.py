#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def stripe_get_handle(handle):
    """stripe_get_handle returns the Stripe handle.

       :rtype: Stripe Handle
    """
    return handle
