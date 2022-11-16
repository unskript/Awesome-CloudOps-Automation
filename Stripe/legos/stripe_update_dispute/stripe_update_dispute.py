##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Any

from pydantic import BaseModel, Field
class InputSchema(BaseModel):
    dispute_id: str = Field(
        title='Dispute Id',
        description='Dispute Id'
    )
    submit: bool = Field(
        False,
        title='Submit',
        description='Whether to immediately submit evidence to the bank.'
    )
    metadata: dict = Field(
        None,
        title='Metadata',
        description='This can be useful for storing additional information about the object in a structured format. '
                    'For Eg. {"order_id": "6735"}'
    )
    evidence: dict = Field(
        None,
        title='Evidence',
        description='Evidence to upload, to respond to a dispute.'
    )


pp = pprint.PrettyPrinter(indent=2)


def legoPrinter(func):
    def Printer(*args, **kwargs):
        update_dispute = func(*args, **kwargs)
        print('\n\n')
        pp.pprint(update_dispute)
        return update_dispute
    return Printer


@legoPrinter
def stripe_update_dispute(handle,
                          dispute_id:str,
                          submit:bool=False,
                          metadata=None,
                          evidence=None) -> Any:
    """stripe_update_dispute Update a Dispute.

        :type dispute_id: string
        :param dispute_id: Dispute Id

        :type submit: bool
        :param submit: Whether to immediately submit evidence to the bank.

        :type metadata: dict
        :param metadata: This can be useful for storing additional information about the object in a structured format.

        :type evidence: dict
        :param evidence: Evidence to upload, to respond to a dispute.

        :rtype: String with response from the describe command.
    """
    # Input param validation

    if evidence is None:
        evidence = {}
    if metadata is None:
        metadata = {}
    try:
        dispute = handle.Dispute.modify(
             dispute_id,
             submit = submit if submit else None,
             metadata = metadata if metadata else {},
             evidence = evidence if evidence else {},
        )
        return dispute
    except Exception as e:
        pp.pprint(e)

    return None
