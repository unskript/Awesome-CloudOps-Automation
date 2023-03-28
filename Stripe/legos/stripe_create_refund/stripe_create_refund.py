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


def stripe_create_refund_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


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
        pprint.pprint(e)

    return None
