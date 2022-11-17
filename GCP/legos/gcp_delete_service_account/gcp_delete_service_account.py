##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
import pprint
from typing import Dict
from googleapiclient import discovery


class InputSchema(BaseModel):
    sa_id: str = Field(
        title = "Service Account Email",
        description = "Email of the service account"
    )


def gcp_delete_service_account_printer(output):
    if output is None:
        return
    pprint(output)


def gcp_delete_service_account(handle, sa_id: str) -> Dict:
    """gcp_delete_service_account Returns a Dict of success detailsfor the deleted service account

        :type sa_id: string
        :param sa_id: Email of the service account

        :rtype: Dict
    """
    service = discovery.build(
        'iam', 'v1', credentials=handle)

    result = {}
    try:
        service.projects().serviceAccounts().delete(
            name='projects/-/serviceAccounts/' + sa_id).execute()

        result["Success"] = "Account with name {} deleted successfuly".format(email)

    except Exception as error:
        result = {"error": error}

    return result