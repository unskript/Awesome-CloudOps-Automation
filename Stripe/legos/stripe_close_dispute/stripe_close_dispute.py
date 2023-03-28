##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from typing import Any


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



def stripe_close_dispute(handle, dispute_id:str) -> Any:
    """stripe_close_dispute Close Dispute

        :type dispute_id: string
        :param dispute_id: Dispute ID

        :rtype: String with response from the describe command.
    """
    # Input param validation
    try:
        resp = handle.Dispute.close(dispute_id)
        return resp
    except Exception as e:
        pprint.pprint(e)

    return None
