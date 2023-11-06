#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import List
from tabulate import tabulate
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def keycloak_get_audit_report_printer(output):
    if not output:
        print("No audit events found.")
        return

    # Extract relevant event data for tabulation
    table_data = []
    for event in output:
        table_data.append({
            "Time": event['time'],
            "Type": event['type'],
            "User ID": event['userId'],
            "Client ID": event['clientId'],
            "IP Address": event['ipAddress'],
            "Error": event.get('error', '')
        })

    # Convert list of dictionaries to tabulated format
    headers = ["Time", "Type", "User ID", "Client ID", "IP Address", "Error"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


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
        raise e


