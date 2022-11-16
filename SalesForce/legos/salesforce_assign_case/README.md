[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Assign Salesforce Case</h2>

<br>

## Description
This Lego Assign a Salesforce case.


## Lego Details

    salesforce_assign_case(handle: object, case_number: str, owner_id: str)

        handle: Object of type unSkript Salesforce Connector
        case_number: The Case number to get the details about the case
        owner_id: User to assign the case to. Eg user@acme.com

## Lego Input
This Lego take three inputs handle, case_number and owner_id.

## Lego Output
Here is a sample output.

    unskript/legos/salesforce/salesforce_assign_case/test_salesforce_assign_case.py::test_salesforce_assign_case
    ----SETTING UP TEST----
    Case 00001097 assigned successfully

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)