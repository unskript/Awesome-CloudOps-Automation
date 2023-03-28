##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from pydantic import BaseModel
from typing import List

class InputSchema(BaseModel):
    pass


def stripe_get_all_customers_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


def stripe_get_all_customers(handle) -> List:
    """stripe_get_all_customers Returns a list of customers that was perviously created. The
        charges are returned in sorted order, with the most recent charges appearing first.

        :rtype: Returns the results of all recent charges.
    """
    # Input param validation.
    output = handle.Customer.list()
    return output["data"]