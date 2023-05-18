##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    charge_id: str = Field(
        title='Charge Id',
        description='Charge ID'
    )


def stripe_retrieve_charge_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


def stripe_retrieve_charge(handle, charge_id:str) -> Dict:
    """stripe_retrive_charge Retrive the Charge for given ID

        :type charge_id: string
        :param charge_id: Charge ID.

        :rtype: Dict with response from the describe API.
    """
    # Input param validation
    charge = handle.Charge.retrieve(charge_id)
    return charge
