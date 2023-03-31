##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
import pprint
from typing import List
import googleapiclient.discovery


class InputSchema(BaseModel):
    project_id: str = Field(
        title = "Project ID",
        description = "Name of the project e.g unskript-dev"
    )

def gcp_list_service_accounts_printer(output):
    if output is None:
        return
    pprint(output)

def gcp_list_service_accounts(handle, project_id: str) -> List:
    """gcp_list_service_accounts Returns a list of service accounts

        :type project_id: string
        :param project_id: Name of the project

        :rtype: List of service accounts
    """
    result = []
    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=handle)
    try:
        service_accounts = service.projects().serviceAccounts().list(
            name='projects/' + project_id).execute()

        for account in service_accounts["accounts"]:
            result.append(account["name"])

    except Exception as error:
        result.append(error)

    return result
