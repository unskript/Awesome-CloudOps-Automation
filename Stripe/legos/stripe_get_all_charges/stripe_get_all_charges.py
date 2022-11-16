##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import Tuple

from pydantic import BaseModel
from tabulate import tabulate

class InputSchema(BaseModel):
    pass


def legoPrinter(func):
    def Printer(*args, **kwargs):
        od, data = func(*args, **kwargs)
        print('\n')
        print(od)
        print('\n')
        print(data)
        return od, data
    return Printer


@legoPrinter
def stripe_get_all_charges(handle) -> Tuple:
    """stripe_get_all_charges Returns a list of charges that was previously created. The
        charges are returned in sorted order, with the most recent charges appearing first.
        
        :rtype: Returns the results of all recent charges.
    """


    data = handle.Charge.list(limit=10)
    op = []
    for item in data:
        op.append([item['amount'], item['id'], item['description']])

    od = tabulate(op, headers=['Amount', 'ID', 'Description'])
    return od, data
