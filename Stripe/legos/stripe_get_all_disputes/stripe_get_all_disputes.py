##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from pydantic import BaseModel
from typing import Dict, List


class InputSchema(BaseModel):
     max_results: int = Field(
        title='Maximum Results',
        description='Threshold to get maximum result.'
    )


def stripe_get_all_disputes_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


def stripe_get_all_disputes(handle, max_results: int = 25) -> List:
    """stripe_get_all_disputes Returns a list of disputes that was perviously created.

        :type max_results: int
        :param max_results: Threshold to get maximum result.

        rtype: Returns a list of disputes that was perviously created.
    """
    result = []
    try:
        if max_results == 0:
            output = handle.Dispute.list()
            result = output["data"]
        else:
            output = handle.Dispute.list(limit=max_results)
            result = output["data"]
    except Exception as e:
        print(e)

    return result
