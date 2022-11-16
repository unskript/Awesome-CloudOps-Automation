##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from typing import Any

class InputSchema(BaseModel):
    params: dict = Field(
        title='Customer Data',
        description='Params in key=value form.'
    )


pp = pprint.PrettyPrinter(indent=2)


def legoPrinter(func):
    def Printer(*args, **kwargs):
        customer = func(*args, **kwargs)
        print('\n')
        pp.pprint(customer)
        return customer
    return Printer


@legoPrinter
def stripe_create_customer(handle, params:dict) -> Any:
    """stripe_create_customer Create a customer

        :type params: dict
        :param params: Params in key=value form.

        :rtype: String with response from the describe command.
    """
    # Input param validation

    try:
        customer = handle.Customer.create(**params)
        return customer
    except Exception as e:
        pp.pprint(e)

    return None
