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


def stripe_delete_customer_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


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
        pprint.pprint(e)

    return None
