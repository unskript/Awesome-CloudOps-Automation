[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Update a Charge</h2>

<br>

## Description
This Lego Updates the specified charge by setting the values of the parameters passed.
        Any parameters not provided will be left unchanged.


## Lego Details

    stripe_close_dispute(handle: object, charge_id: str, customer: str, description: str,
        receipt_email: str, metadata: dict, shipping: dict, fraud_details: dict,
        transfer_group: str)

        handle: Object of type unSkript stripe Connector
        charge_id: Charge ID.
        customer: Customer ID.
        description: Description
        receipt_email: This is the email address that the receipt for this charge will be sent to
        metadata: This can be useful for storing additional information about the object in a structured format.
        shipping: Shipping information for the charge. Helps prevent fraud on charges for physical goods.
        raud_details: A set of key-value pairs you can attach to a charge giving information about its riskiness
        transfer_group: A string that identifies this transaction as part of a group.


## Lego Input
This Lego take nine input handle, charge_id, customer, description, receipt_email, metadata, shipping, raud_details and transfer_group.

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)