##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def vault_get_handle(handle):
    """vault_get_handle returns the Vault handle.

          :rtype: Vault handle.
    """
    return handle
