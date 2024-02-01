#
# Copyright (c) 2024 unSkript.com
# All rights reserved.
#

import requests

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
        try:
            # Exception could occur if keycloak package was not found
            # in such case try if we can import UnskriptKeycloakWrapper
            from unskript.connectors.keycloak import UnskriptKeycloakWrapper
            from unskript.legos.utils import get_keycloak_token
        except:
            raise e
        
        if not isinstance(handle, UnskriptKeycloakWrapper):
            raise ValueError(f"Unable to Find Keycloak Package! {e}")
        
        access_token = get_keycloak_token(handle)
        realms_url = f"{handle.server_url}/admin/realms"
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
