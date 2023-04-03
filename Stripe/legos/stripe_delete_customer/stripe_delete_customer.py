##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
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


def stripe_delete_customer(handle, customer_id:str) -> List:
    """stripe_delete_customer Delete Customer

        :type customer_id: string
        :param customer_id: Customer Id.

        :rtype: List with response from the describe API.
    """
    # Input param validation
    result = []
    try:
        resp = handle.Customer.delete(customer_id)
        result.append(resp)
        return result
    except Exception as e:
        pprint.pprint(e)

    return None
