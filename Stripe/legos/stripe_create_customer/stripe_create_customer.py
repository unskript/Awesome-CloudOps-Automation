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


def stripe_create_customer_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)



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
        pprint.pprint(e)

    return None
