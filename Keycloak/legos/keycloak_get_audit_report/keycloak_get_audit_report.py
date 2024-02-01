#
# Copyright (c) 2024 unSkript.com
# All rights reserved.
#
import requests

from typing import List
from tabulate import tabulate
from pydantic import BaseModel
from datetime import datetime


class InputSchema(BaseModel):
    pass


def keycloak_get_audit_report_printer(output):
    if not output:
        print("No audit events found.")
        return

    # Extract relevant event data for tabulation
    table_data = [["Time", "Type", "User ID", "Client ID", "IP Address", "Error"]]
    for event in output:
        time = event.get('time') if event.get('time') else ''
        _type = event.get('type') if event.get('type') else \
               event.get('operationType') if event.get('operationType') else ''
        user_id = event.get('userId') if event.get('userId') else \
                  event.get('authDetails').get('userId', '') if event.get('authDetails') else ''
        client_id = event.get('clientId') if event.get('clientId') else \
                  event.get('authDetails').get('clientId', '') if event.get('authDetails') else ''
        ip_addr = event.get('ipAddress') if event.get('ipAddress') else \
                  event.get('authDetails').get('ipAddress', '') if event.get('authDetails') else ''
        error = event.get('error', '')
        
        table_data.append([datetime.fromtimestamp(time/1000).strftime('%Y-%m-%d %H:%M:%S'), 
                           _type, 
                           user_id, 
                           client_id, 
                           ip_addr, 
                           error])

    print(tabulate(table_data, headers='firstrow', tablefmt="grid"))


def keycloak_get_audit_report(handle) -> List:
    """
    keycloak_get_audit_report fetches the audit events from Keycloak.

    :type handle: KeycloakAdmin
    :param handle: Handle containing the KeycloakAdmin instance.

    :rtype: List of dictionaries representing the audit events.
    """
    try:
        # Fetch the events
        events = handle.get_events()
        return events if events else []

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
        events_url = f"{handle.server_url}/admin/realms/{handle.realm_name}/events"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(events_url, headers=headers)
        response.raise_for_status()

        events = response.json()

        return events if events else []
        

