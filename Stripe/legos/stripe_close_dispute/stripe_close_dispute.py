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


pp = pprint.PrettyPrinter(indent=2)


def legoPrinter(func):
    def Printer(*args, **kwargs):
        output = func(*args, **kwargs)
        print('\n')
        pp.pprint(output)
        return output
    return Printer


@legoPrinter
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
        pp.pprint(e)

    return None
