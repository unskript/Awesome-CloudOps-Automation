##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List
from pydantic import BaseModel, Field
from tabulate import tabulate

class InputSchema(BaseModel):
    max_results: int = Field(
        title='Maximum Results',
        description='Threshold to get maximum result.'
    )


def stripe_get_all_charges_printer(output):
    if output is None:
        return
    od = tabulate(output, headers=['Amount', 'ID', 'Description'])
    print(od)



def stripe_get_all_charges(handle, max_results: int = 25) -> List:
    """stripe_get_all_charges Returns a list of charges that was previously created. The
        charges are returned in sorted order, with the most recent charges appearing first.

        :type max_results: int
        :param max_results: Threshold to get maximum result.

        :rtype: Returns the results of all recent charges.
    """
    result = []
    try:
        if max_results == 0:
            data = handle.Charge.list()
            for charge in data.auto_paging_iter():
                result.append([charge['amount'], charge['id'], charge['description']])
        else:
            data = handle.Charge.list(limit=max_results)
            for charge in data:
                result.append([charge['amount'], charge['id'], charge['description']])
    except Exception as e:
        print(e)

    return result
