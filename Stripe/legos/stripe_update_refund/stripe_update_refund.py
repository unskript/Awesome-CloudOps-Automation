##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Any

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

pp = pprint.PrettyPrinter(indent=2)


def legoPrinter(func):
    def Printer(*args, **kwargs):
        update_refund = func(*args, **kwargs)
        print('\n\n')
        pp.pprint(update_refund)
        return update_refund
    return Printer


@legoPrinter
def stripe_update_refund(handle, refund_id:str, metadata:dict) -> Any:
    """stripe_update_refund Updates the specified refund by setting the values of the parameters passed.
        
        :type metadata: dict
        :param metadata: Updates the specified refund by setting the values of the parameters passed.
        
        :type refund_id: string
        :param refund_id: Refund Id
        :rtype: String with response from the describe command.
    """
    # Input param validation


    try:
        refund = handle.Refund.modify(
            refund_id,
            metadata=metadata,
        )
        return refund
    except Exception as e:
        pp.pprint(e)

    return None
