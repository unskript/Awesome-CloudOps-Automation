##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def keycloak_get_handle(handle):
    """keycloak_get_handle returns the Keycloak handle.

          :rtype: Keycloak handle.
    """
    return handle
