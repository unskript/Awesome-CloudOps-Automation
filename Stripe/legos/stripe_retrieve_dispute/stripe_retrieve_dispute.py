##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
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


def stripe_retrieve_dispute(handle, dispute_id:str) -> List:
    """stripe_retrieve_dispute Get Dispute data

        :type dispute_id: string
        :param dispute_id: Retrieve details of a dispute.

        :rtype: List with response from the describe API.
    """
    result = []
    try:
        resp = handle.Dispute.retrieve(dispute_id)
        result.append(resp)
        return result
    except Exception as e:
        pp.pprint(e)

    return None
