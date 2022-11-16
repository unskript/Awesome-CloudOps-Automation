##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Any

from pydantic import BaseModel, Field
class InputSchema(BaseModel):
    charge_id: str = Field(
        title='Charge Id',
        description='The identifier of the charge to refund.'
    )


pp = pprint.PrettyPrinter(indent=2)


def legoPrinter(func):
    def Printer(*args, **kwargs):
        refund_obj = func(*args, **kwargs)
        if refund_obj:
            print('\n\n')
            pp.pprint(refund_obj)
            return refund_obj
        else:
            return None
    return Printer


@legoPrinter
def stripe_create_refund(handle, charge_id:str) -> Any:
    """stripe_create_refund Create a Refund

        :type charge_id: string
        :param charge_id: The identifier of the charge to refund.

        :rtype: String with response from the describe command.
    """
    # Input param validation

    try:
        refund_obj = handle.Refund.create(charge=charge_id)
        return refund_obj
    except Exception as e:
        print('\n\n')
        pp.pprint(e)

    return None
