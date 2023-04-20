##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    refund_id: str = Field(
        title='Refund Id',
        description='The identifier of the refund.'
    )


def stripe_retrieve_refund_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


def stripe_retrieve_refund(handle, refund_id:str) -> List:
    """stripe_retrieve_refund Retrieve a refund

        :type refund_id: string
        :param refund_id: The identifier of the refund.

        :rtype: List with response from the describe API.
    """
    result = []
    try:
        refund_obj = handle.Refund.retrieve(refund_id)
        result.append(refund_obj)
        return result
    except Exception as e:
        pprint.pprint(e)

    return None
