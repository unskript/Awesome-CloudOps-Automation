##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Any

from pydantic import BaseModel, Field
class InputSchema(BaseModel):
    customer_id: str = Field(
        title='Customer Id',
        description='Retrive details of a customer'
    )

pp = pprint.PrettyPrinter(indent=2)


def legoPrinter(func):
    def Printer(*args, **kwargs):
        retrieve_customer = func(*args, **kwargs)
        print('\n\n')
        pp.pprint(retrieve_customer)
        return retrieve_customer
    return Printer


@legoPrinter
def stripe_retrieve_customer(handle, customer_id:str) -> Any:
    """stripe_retrieve_customer Get customer data

        :type customer_id: string
        :param customer_id: Retrive details of a customer.

        :rtype: String with response from the describe command.
    """
    # Input param validation

    try:
        customer = handle.Customer.retrieve(customer_id)
        return customer
    except Exception as e:
        pp.pprint(e)

    return None
