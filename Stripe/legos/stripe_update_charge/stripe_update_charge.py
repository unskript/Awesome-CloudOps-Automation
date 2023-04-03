##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List, Dict
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    charge_id: str = Field(
        title='Charge Id',
        description='Charge ID'
    )
    customer: str = Field(
        title='Customer Id',
        description='Customer ID'
    )
    description: str = Field(
        title='Description',
        description='Description'
    )
    receipt_email: str = Field(
        title='Email address ',
        description='This is the email address that the receipt for this charge will be sent to'
    )
    metadata: dict = Field(
        None,
        title='Metadata',
        description='This can be useful for storing additional information about the object in a structured format. '
                    'For Eg. {"order_id": "6735"}'
    )
    shipping: dict = Field(
        None,
        title='Shipping Details',
        description='Shipping information for the charge. Helps prevent fraud on charges for physical goods.'
    )
    fraud_details: dict = Field(
        None,
        title='Fraud Details',
        description='A set of key-value pairs you can attach to a charge giving information about its riskiness'
    )
    transfer_group: str = Field(
        None,
        title='Transfer Group',
        description='A string that identifies this transaction as part of a group.'
    )


def stripe_update_charge_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


def stripe_update_charge(
        handle,
        charge_id: str,
        customer: str,
        description: str,
        receipt_email: str,
        metadata: dict = {},
        shipping: dict = {},
        fraud_details: dict = {},
        transfer_group: str = "") -> List:

    """stripe_update_charge Updates the specified charge by setting the values of the parameters passed.
        Any parameters not provided will be left unchanged.

        :type charge_id: string
        :param charge_id: Charge ID.

        :type customer: string
        :param customer: Customer ID.

        :type description: string
        :param description: Description

        :type receipt_email: string
        :param receipt_email: This is the email address that the receipt for this charge will be sent to

        :type metadata: dict
        :param metadata: This can be useful for storing additional information about the object in a structured format.

        :type shipping: dict
        :param shipping: Shipping information for the charge. Helps prevent fraud on charges for physical goods.

        :type fraud_details: dict
        :param fraud_details: A set of key-value pairs you can attach to a charge giving information about its riskiness

        :type transfer_group: string
        :param transfer_group: A string that identifies this transaction as part of a group.

        :rtype: String with response from the describe command.
    """
    # Input param validation
    result = []
    try:
        charge = handle.Charge.modify(
            charge_id,
            customer=customer if customer else None,
            description=description if description else None,
            metadata=metadata if metadata else {},
            receipt_email=receipt_email if receipt_email else None,
            shipping=shipping if shipping else None,
            fraud_details=fraud_details if fraud_details else None,
            transfer_group=transfer_group if transfer_group else None,
        )
        result.append(charge)
        return result
    except Exception as e:
        pprint.pprint(e)

    return None
