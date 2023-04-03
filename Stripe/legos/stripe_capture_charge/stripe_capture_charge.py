##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from typing import List

class InputSchema(BaseModel):
    charge_id: str = Field(
        title='Charge Id',
        description='Capture the payment of an existing, uncaptured, charge'
    )


def stripe_capture_charge_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)



def stripe_capture_charge(handle, charge_id:str) -> List:
    """stripe_capture_charge Capture the payment of an existing, uncaptured, charge.

        :type charge_id: string
        :param charge_id: Capture the payment of an existing, uncaptured, charge.

        :rtype: List with response from the describe API.
    """
    # Input param validation
    result = []
    try:
        charge = handle.Charge.capture(charge_id)
        result.append(charge)
        return result
    except Exception as e:
        pprint.pprint(e)

    return None
