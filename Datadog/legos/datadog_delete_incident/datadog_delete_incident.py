##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client import ApiClient
from typing import Dict
import pprint

class InputSchema(BaseModel):
    incident_id: str = Field(
        title='Incident Id',
        description='Id of the incident to delete.')

def datadog_delete_incident_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def datadog_delete_incident(handle, incident_id: str) -> None:
    """datadog_delete_incident deletes an incident given its id.

        :type name: str
        :param incident_id: Id of the incident to delete.

        :rtype: None
    """
    try:
        handle.handle_v2.unstable_operations["delete_incident"] = True
        with ApiClient(handle.handle_v2) as api_client:
            api_instance = IncidentsApi(api_client)
            deleted_incident = api_instance.delete_incident(incident_id=incident_id)
    except Exception as e:
        raise e
    return deleted_incident