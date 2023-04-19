##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from typing import Dict, List


class InputSchema(BaseModel):
    max_results: int = Field(
        title='Maximum Results',
        description='Threshold to get maximum result.'
    )


def stripe_get_all_refunds_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


def stripe_get_all_refunds(handle, max_results: int = 25) -> List:
    """stripe_get_all_refunds Returns a list of refunds that was previously created. The
        charges are returned in sorted order, with the most recent charges appearing first.

        :type max_results: int
        :param max_results: Threshold to get maximum result.

        :rtype: Returns the results of all recent charges.
    """
    result = []
    if max_results == 0:
        output = handle.Refund.list()
        for refunds in output.auto_paging_iter():
            result.append(refunds)
    else:
        output = handle.Refund.list(limit=max_results)
        for refunds in output:
            result.append(refunds)

    return result
