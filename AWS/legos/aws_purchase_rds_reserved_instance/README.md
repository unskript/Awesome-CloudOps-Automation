[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">]
(https://unskript.com/assets/favicon.png)
<h1>AWS Purchase RDS Reserved Instances</h1>

## Description
This action purchases a reserved DB instance offering.

## Lego Details
	aws_purchase_rds_reserved_instance(handle, region: str, reserved_instance_offering_id: str, db_instance_count:int=1)
		handle: Object of type unSkript AWS Connector.
		reserved_instance_offering_id: The unique identifier of the reserved instance offering you want to purchase.
		db_instance_count: The number of reserved instances that you want to purchase.

## Lego Input
This Lego takes inputs handle, reserved_instance_offering_id, db_instance_count.

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)