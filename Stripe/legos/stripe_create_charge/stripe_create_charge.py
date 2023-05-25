##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from typing import Optional, List
from pydantic import BaseModel, Field
from tabulate import tabulate

class InputSchema(BaseModel):
    amount: int = Field(
        title='Amount',
        description='Amount intended to be collected by this payment')
    currency: Optional[str] = Field(
        'usd',
        title='Currency',
        description='Three letter ISO currency code, eg: usd, cad, eur')
    source: Optional[str] = Field(
        title='Payment Source',
        description='A payment source to be charged. eg. credit card ID, bank account, token')
    description: Optional[str] = Field(
        title='Description',
        description='Reason for the Charge. Small Description about charge.')


def stripe_create_charge_printer(output):
    if output is None:
        return
    od = tabulate(output, headers=['Amount', 'ID', 'Description'])
    print(od)



def stripe_create_charge(
        handle,
        amount: int,
        source: str = "",
        description: str = "",
        currency: str = "usd"
        ) -> List:
    """stripe_create_charge Charges a credit card or other payment source to the given amount
        in the given currency.
        
        :type amount: int
        :param amount: Amount intended to be collected by this payment.

        :type source: str
        :param source: A payment source to be charged.

        :type description: str
        :param description: Reason for the Charge. Small Description about charge.

        :type currency: str
        :param currency: Three letter ISO currency code, eg: usd, cad, eur

        :rtype: Returns the results of all recent charges.
    """
    # Input param validation.
    result = []
    try:
        data = handle.Charge.create(
            amount=amount,
            currency=currency,
            source=source,
            description=description)
        result.append([str(data['amount']), data['id'], data['description']])
    except Exception:
        data = 'Error occurred when Creating a charge'
        print(data)

    return result
