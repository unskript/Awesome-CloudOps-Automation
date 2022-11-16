[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Create a Charge</h2>

<br>

## Description
This Lego used to Charges a credit card or other payment source to the given amount
        in the given currency.


## Lego Details

    stripe_close_dispute(handle: object, amount: int, source: str, description: str, currency: str)

        handle: Object of type unSkript stripe Connector
        amount: Amount intended to be collected by this payment.
        source: A payment source to be charged.
        description: Reason for the Charge. Small Description about charge.
        currency: Three letter ISO currency code, eg: usd, cad, eur

## Lego Input
This Lego take five input handle, amount, source, description and currency.

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)