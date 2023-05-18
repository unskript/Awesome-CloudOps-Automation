##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    dispute_id: str = Field(
        title='Dispute ID',
        description='Dispute ID'
    )


def stripe_close_dispute_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)



def stripe_close_dispute(handle, dispute_id:str) -> List:
    """stripe_close_dispute Close Dispute

        :type dispute_id: string
        :param dispute_id: Dispute ID

        :rtype: List with response from the describe API.
    """
    # Input param validation
    result = []
    try:
        resp = handle.Dispute.close(dispute_id)
        result.append(resp)
        return result
    except Exception as e:
        pprint.pprint(e)

    return None
