##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from pydantic import BaseModel, Field
from typing import Optional, Tuple
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


def legoPrinter(func):
    def Printer(*args, **kwargs):
        od, data = func(*args, **kwargs)
        print('\n')
        print(od)
        print('\n\n', "* More details can be found in data variable", type(data))
        return od, data
    return Printer


@legoPrinter
def stripe_create_charge(handle, amount: int, source: str = "", description: str = "", currency: str = "usd") -> Tuple:
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

    try:
        data = handle.Charge.create(
            amount=amount,
            currency=currency,
            source=source,
            description=description)
    except Exception as e:
        od = e
        data = 'Error occurred when Creating a charge'
    else:
        od = tabulate([[str(data['amount']), data['id'], data['description']]], headers=[
            'Amount', 'ID', 'Description'])

    return od, data
