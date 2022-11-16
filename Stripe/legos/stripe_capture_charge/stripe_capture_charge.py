##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from typing import Any

class InputSchema(BaseModel):
    charge_id: str = Field(
        title='Charge Id',
        description='Capture the payment of an existing, uncaptured, charge'
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
def stripe_capture_charge(handle, charge_id:str) -> Any:
    """stripe_capture_charge Capture the payment of an existing, uncaptured, charge.

        :type charge_id: string
        :param charge_id: Capture the payment of an existing, uncaptured, charge.

        :rtype: String with response from the describe command.
    """
    # Input param validation

    try:
        charge = handle.Charge.capture(charge_id)
        return charge
    except Exception as e:
        pp.pprint(e)

    return None
