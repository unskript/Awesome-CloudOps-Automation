##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    charge_id: str = Field(
        title='Charge Id',
        description='The identifier of the charge to refund.'
    )


def stripe_create_refund_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


def stripe_create_refund(handle, charge_id:str) -> List:
    """stripe_create_refund Create a Refund

        :type charge_id: string
        :param charge_id: The identifier of the charge to refund.

        :rtype: List with response from the describe API.
    """
    # Input param validation
    result = []
    try:
        refund_obj = handle.Refund.create(charge=charge_id)
        result.append(refund_obj)
        return result
    except Exception as e:
        pprint.pprint(e)

    return None
