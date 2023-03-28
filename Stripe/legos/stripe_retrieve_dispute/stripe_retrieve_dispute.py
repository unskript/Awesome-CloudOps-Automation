##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Any
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    dispute_id: str = Field(
        title='Dispute Id',
        description='Retrieve details of a dispute'
    )


def stripe_retrieve_dispute_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


def stripe_retrieve_dispute(handle, dispute_id:str) -> Any:
    """stripe_retrieve_dispute Get Dispute data

        :type dispute_id: string
        :param dispute_id: Retrieve details of a dispute.

        :rtype: String with response from the describe command.
    """
    try:
        resp = handle.Dispute.retrieve(dispute_id)
        return resp
    except Exception as e:
        pp.pprint(e)

    return None
