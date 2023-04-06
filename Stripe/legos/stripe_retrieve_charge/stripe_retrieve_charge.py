##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from typing import Dict

class InputSchema(BaseModel):
    charge_id: str = Field(
        title='Charge Id',
        description='Charge ID'
    )


pp = pprint.PrettyPrinter(indent=2)


def legoPrinter(func):
    def Printer(*args, **kwargs):
        retrieve_charge = func(*args, **kwargs)
        print('\n\n')
        pp.pprint(retrieve_charge)
        return retrieve_charge
    return Printer


@legoPrinter
def stripe_retrieve_charge(handle, charge_id:str) -> Dict:
    """stripe_retrieve_charge Retrieve the Charge for given ID

        :type charge_id: string
        :param charge_id: Charge ID.

        :rtype: String with response from the describe command.
    """
    # Input param validation

    charge = handle.Charge.retrieve(charge_id)
    return charge
