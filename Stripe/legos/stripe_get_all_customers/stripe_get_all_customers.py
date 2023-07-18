##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    max_results: int = Field(
        title='Maximum Results',
        description='Threshold to get maximum result.'
    )


def stripe_get_all_customers_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


def stripe_get_all_customers(handle, max_results: int = 25) -> List:
    """stripe_get_all_customers Returns a list of customers that was perviously created.

        :type max_results: int
        :param max_results: Threshold to get maximum result.

        :rtype: Returns the results of all customers.
    """
    # Input param validation.
    result = []
    try:
        if max_results == 0:
            output = handle.Customer.list(limit=100)
            for customer in output.auto_paging_iter():
                result.append(customer)
        else:
            output = handle.Customer.list(limit=max_results)
            result = output["data"]
    except Exception as e:
        print(e)

    return result
