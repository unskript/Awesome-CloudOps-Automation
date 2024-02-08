#
# Copyright (c) 2024 unSkript.com
# All rights reserved.
#

import requests
import os 

from typing import Tuple
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass

def keycloak_get_service_health(handle):
    """
    keycloak_get_service_health fetches the health of the Keycloak service by trying to list available realms.

    :type handle: object
    :param handle: Handle containing the KeycloakAdmin instance.

    :rtype: Tuple indicating if the service is healthy and a list of available realms (or None if healthy).
    """
    try:
        from unskript.connectors.keycloak import UnskriptKeycloakWrapper
        from unskript.legos.utils import get_keycloak_token
        
        if not isinstance(handle, UnskriptKeycloakWrapper):
            raise ValueError("Unable to Find Keycloak Package!")
        
        access_token = get_keycloak_token(handle)
        realms_url = os.path.join(handle.server_url, "admin/realms")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(realms_url, headers=headers)
        response.raise_for_status()

        available_realms = response.json()
        result = False
        if handle.realm_name and available_realms:
            result = any(realm.get("realm") == handle.realm_name for realm in available_realms)

        if not result:
            return (False, available_realms)
        
        return (True, None)
    except Exception as e:
        print(f"ERROR: Unable to connect to keycloak server {str(e)}")



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
