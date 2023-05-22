##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field

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


def stripe_create_customer(handle, params:dict) -> List:
    """stripe_create_customer Create a customer

        :type params: dict
        :param params: Params in key=value form.

        :rtype: List with response from the describe API.
    """
    # Input param validation
    result = []
    try:
        customer = handle.Customer.create(**params)
        result.append(customer)
        return result
    except Exception as e:
        pprint.pprint(e)

    return None
