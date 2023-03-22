##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from datadog_api_client.v1.api.events_api import EventsApi
from datadog_api_client import ApiClient
from typing import Dict
import pprint


class InputSchema(BaseModel):
    event_id: int = Field(
        title='event Id',
        description='Id of the event to retrieve.')


def datadog_get_event_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def datadog_get_event(handle, event_id: int) -> Dict:
    """datadog_get_event gets an event given its id.

        :type event_id: int
        :param event_id: Id of the event to retrieve.

        :rtype: A Dict containing the event
    """
    try:
        with ApiClient(handle.handle_v2) as api_client:
            api_instance = EventsApi(api_client)
            event = api_instance.get_event(event_id=int(event_id))
    except Exception as e:
        raise e
    return event.to_dict()