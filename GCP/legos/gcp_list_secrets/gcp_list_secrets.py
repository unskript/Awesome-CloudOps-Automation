##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import List
from pydantic import BaseModel, Field
from google.cloud import secretmanager
import pprint

class InputSchema(BaseModel):
    name: str = Field(
        title='Project Name',
        description='Name of the Google Cloud Project.')

def gcp_list_secrets_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def gcp_list_secrets(handle, name: str) -> List:
    """gcp_list_secrets List all the secrets for a given project.

        :type name: string
        :param name: Name of the Google Cloud Project.

        :rtype: List of the names of all the secrets.
    """
    client = secretmanager.SecretManagerServiceClient(credentials=handle)

    # Input param validation.
    parent = "projects/" + name
    try:
            resp = client.list_secrets(parent=parent)
    except Exception as e:
        raise(e)
    output = []
    for i in resp.secrets:
        output.append(i.name)
    return output
