##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    customer_id: str = Field(
        title='Customer Id',
        description='Customer ID'
    )
    name: str = Field(
        title='The customer’s full name or business name.',
        description='The customer’s full name or business name.'
    )
    phone: str = Field(
        title='The customer’s phone number.',
        description='The customer’s phone number.'
    )
    description: str = Field(
        title='Description',
        description='Description'
    )
    email: str = Field(
        title='Email address ',
        description='Customer’s email address'
    )
    balance: int = Field(
        title='Current Balance',
        description='Current Balance'
    )
    metadata: dict = Field(
        None,
        title='Metadata',
        description='This can be useful for storing additional information about the object \
            in a structured format. For Eg. {"order_id": "6735"}'
    )
    shipping: dict = Field(
        None,
        title='Shipping Details',
        description='Shipping information for the customer.'
    )
    address: dict = Field(
        None,
        title='The customer’s address.',
        description='The customer’s address.'
    )


def stripe_update_customer_printer(output):
    if isinstance(output, (list, tuple)):
        pprint.pprint(output)
    elif isinstance(output, dict):
        pprint.pprint(output)
    else:
        pprint.pprint(output)


def stripe_update_customer(
        handle,
        customer_id: str,
        name: str,
        phone: str,
        description: str,
        email: str,
        balance: int,
        metadata: dict,
        shipping: dict,
        address: dict) -> List:
    """stripe_update_customer Update a customer

        :type customer_id: string
        :param customer_id: Customer ID

        :type name: string
        :param name: The customer’s full name or business name.

        :type phone: string
        :param phone: The customer’s phone number.

        :type description: string
        :param description: Description

        :type email: string
        :param email: Customer’s email address

        :type balance: int
        :param balance: Current Balance

        :type metadata: dict
        :param metadata: This can be useful for storing additional information
        about the object in a structured format.

        :type shipping: dict
        :param shipping: Shipping information for the customer.

        :type address: dict
        :param address: The customer’s address.

        :rtype: List with response from the describe API.
    """
    # Input param validation
    result = []
    try:
        customer = handle.Customer.modify(
            customer_id,
            name=name if name else None,
            phone=phone if phone else None,
            description=description if description else None,
            balance=balance if balance else None,
            email=email if email else None,
            metadata=metadata if metadata else {},
            address=address if address else {},
            shipping=shipping if shipping else None,
        )
        result.append(customer)
        return result
    except Exception as e:
        pprint.pprint(e)

    return None
