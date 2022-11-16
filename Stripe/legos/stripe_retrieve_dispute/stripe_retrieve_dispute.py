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


pp = pprint.PrettyPrinter(indent=2)


def legoPrinter(func):
    def Printer(*args, **kwargs):
        retrieve_dispute = func(*args, **kwargs)
        print('\n\n')
        pp.pprint(retrieve_dispute)
        return retrieve_dispute
    return Printer


@legoPrinter
def stripe_retrieve_dispute(handle, dispute_id:str) -> Any:
    """stripe_retrieve_dispute Get Dispute data

        :type dispute_id: string
        :param dispute_id: Retrieve details of a dispute.

        :rtype: String with response from the describe command.
    """
    # Input param validation

    try:
        resp = handle.Dispute.retrieve(dispute_id)
        return resp
    except Exception as e:
        pp.pprint(e)

    return None
