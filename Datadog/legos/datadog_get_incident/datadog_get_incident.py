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
        description='Id of the incident to retrieve.')

def datadog_get_incident_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def datadog_get_incident(handle, incident_id: str) -> Dict:
    """datadog_get_incident gets an incident given its id.

        :type name: str
        :param incident_id: Id of the incident to retrieve.

        :rtype: A Dict containing the incident
    """
    try:
        handle.unstable_operations["get_incident"] = True
        with ApiClient(handle) as api_client:
            api_instance = IncidentsApi(api_client)
            incident = api_instance.get_incident(incident_id=incident_id)
    except Exception as e:
        raise e
    return incident.to_dict()