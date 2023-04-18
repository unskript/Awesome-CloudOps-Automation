##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
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


def stripe_update_dispute_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


def stripe_update_dispute(handle,
                          dispute_id: str,
                          submit: bool = False,
                          metadata=None,
                          evidence=None) -> List:
    """stripe_update_dispute Update a Dispute.

        :type dispute_id: string
        :param dispute_id: Dispute Id

        :type submit: bool
        :param submit: Whether to immediately submit evidence to the bank.

        :type metadata: dict
        :param metadata: This can be useful for storing additional information about the object in a structured format.

        :type evidence: dict
        :param evidence: Evidence to upload, to respond to a dispute.

        :rtype: List with response from the describe API.
    """
    # Input param validation
    result = []
    if evidence is None:
        evidence = {}
    if metadata is None:
        metadata = {}
    try:
        dispute = handle.Dispute.modify(
             dispute_id,
             submit=submit if submit else None,
             metadata=metadata if metadata else {},
             evidence=evidence if evidence else {},
        )
        result.append(dispute)
        return result
    except Exception as e:
        pprint.pprint(e)

    return None