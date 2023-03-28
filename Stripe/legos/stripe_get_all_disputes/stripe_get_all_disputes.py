##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from pydantic import BaseModel
from typing import Dict


class InputSchema(BaseModel):
    pass


def stripe_get_all_disputes_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


def stripe_get_all_disputes(handle) -> Dict:
    """stripe_get_all_disputes Returns a list of disputes that was perviously created. The
        charges are returned in sorted order, with the most recent charges appearing first.

        rtype: Returns a list of disputes that was perviously created.
    """

    output = handle.Dispute.list()
    return output
