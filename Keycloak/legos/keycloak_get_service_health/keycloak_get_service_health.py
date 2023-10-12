#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#

from typing import Tuple
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass

def keycloak_get_service_health(handle) -> Tuple:
    """
    keycloak_get_service_health fetches the health of the Keycloak service by trying to list available realms.

    :type handle: object
    :param handle: Handle containing the KeycloakAdmin instance.

    :rtype: Tuple indicating if the service is healthy and a list of available realms (or None if healthy).
    """
    try:
        realms = handle.get_realms()
        available_realms = [realm["realm"] for realm in realms]
        
        if not available_realms:
            return (False, available_realms)
        
        return (True, None)

    except Exception as e:
        raise e

def keycloak_get_service_health_printer(output):
    is_healthy, realms = output

    if is_healthy:
        print("Keycloak Service is Healthy.")
    else:
        print("Keycloak Service is Unhealthy.")
        if realms:
            print("\nUnavailable Realms:")
            for realm in realms:
                print(f"  - {realm}")
