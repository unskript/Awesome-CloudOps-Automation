##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Any

from pydantic import BaseModel, Field
class InputSchema(BaseModel):
    refund_id: str = Field(
        title='Refund Id',
        description='The identifier of the refund.'
    )


pp = pprint.PrettyPrinter(indent=2)


def legoPrinter(func):
    def Printer(*args, **kwargs):
        retrieve_refund = func(*args, **kwargs)
        print('\n\n')
        pp.pprint(retrieve_refund)
        return retrieve_refund
    return Printer


@legoPrinter
def stripe_retrieve_refund(handle, refund_id:str) -> Any:
    """stripe_retrieve_refund Retrieve a refund

        :type refund_id: string
        :param refund_id: The identifier of the refund.

        :rtype: String with response from the describe command.
    """
    # Input param validation

    try:
        refund_obj = handle.Refund.retrieve(refund_id)
        return refund_obj
    except Exception as e:
        pp.pprint(e)

    return None
