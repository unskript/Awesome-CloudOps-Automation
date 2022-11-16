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
        description='Customer Id'
    )

pp = pprint.PrettyPrinter(indent=2)


def legoPrinter(func):
    def Printer(*args, **kwargs):
        delete_customer = func(*args, **kwargs)
        print('\n\n')
        pp.pprint(delete_customer)
        return delete_customer
    return Printer


@legoPrinter
def stripe_delete_customer(handle, customer_id:str) -> Any:
    """stripe_delete_customer Delete Customer

        :type customer_id: string
        :param customer_id: Customer Id.

        :rtype: String with response from the describe command.
    """
    # Input param validation

    try:
        resp = handle.Customer.delete(customer_id)
        return resp
    except Exception as e:
        pp.pprint(e)

    return None
