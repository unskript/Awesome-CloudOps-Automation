##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List
from pydantic import BaseModel
from tabulate import tabulate

class InputSchema(BaseModel):
    pass


def stripe_get_all_charges_printer(output):
    if output is None:
        return
    od = tabulate(output, headers=['Amount', 'ID', 'Description'])
    print(od)



def stripe_get_all_charges(handle) -> List:
    """stripe_get_all_charges Returns a list of charges that was previously created. The
        charges are returned in sorted order, with the most recent charges appearing first.

        :rtype: Returns the results of all recent charges.
    """
    data = handle.Charge.list(limit=10)
    op = []
    for item in data:
        op.append([item['amount'], item['id'], item['description']])

    return op
