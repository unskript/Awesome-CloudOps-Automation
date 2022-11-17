##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
import pprint
from typing import List,Any, Dict
from google.oauth2 import service_account
import googleapiclient.discovery


class InputSchema(BaseModel):
    project_id: str = Field(
        title = "Project ID",
        description = "Name of the project e.g unskript-dev"
    )
    accountId: str = Field(
        title = "Account ID",
        description = "Name for the service account e.g test-account"
    )
    display_name: str = Field(
        title = "Display Name",
        description = "Display Name for the service account e.g test-account"
    )

def gcp_create_service_account_printer(output):
    if output is None:
        return
    pprint(output)

def gcp_create_service_account(handle, project_id: str, accountId: str, display_name:str) -> Dict:
    """gcp_create_service_account Returns a Dict of details of the created service account

        :type project_id: string
        :param project_id: Name of the project

        :type accountId: string
        :param accountId: Name for the service account

        :type display_name: string
        :param display_name: Display Name for the service account

        :rtype: Dict of details of the created service account
    """
    """Creates a service account."""
    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=handle)

    result = {}
    try:
        response = service.projects().serviceAccounts().create(
            name='projects/' + project_id,
            body={
                'accountId': accountId,
                'serviceAccount': {
                    'displayName': display_name
                }}).execute()
        result = response

    except Exception as error:
        result = {"error": error}

    return result