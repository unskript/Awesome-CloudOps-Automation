##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    refund_id:str = Field(
        title='Refund Id',
        description='Refund Id'
    )
    metadata: dict = Field(
        title='Metadata',
        description='''
                    Updates the specified refund by setting the values of the parameters passed.
                    For Eg. {"order_id": "6735"}'
                    '''
    )

def stripe_update_refund_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


def stripe_update_refund(handle, refund_id:str, metadata:dict) -> List:
    """stripe_update_refund Updates the specified refund by setting the values of the parameters passed.

        :type metadata: dict
        :param metadata: Updates the specified refund by setting the values of the parameters passed.

        :type refund_id: string
        :param refund_id: Refund Id
        
        :rtype: List with response from the describe API.
    """
    # Input param validation
    result = []
    try:
        refund = handle.Refund.modify(
            refund_id,
            metadata=metadata,
        )
        result.append(refund)
        return result
    except Exception as e:
        pprint.pprint(e)

    return None