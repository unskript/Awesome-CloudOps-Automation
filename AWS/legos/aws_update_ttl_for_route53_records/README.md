[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">]
(https://unskript.com/assets/favicon.png)
<h1>AWS Update TTL for Route53 Record</h1>

## Description
Update TTL for an existing record in a hosted zone.

## Lego Details
	aws_update_ttl_for_route53_records(handle, hosted_zone_id: str, record_name: str, record_type:str, new_ttl:int )

		handle: Object of type unSkript AWS Connector.
		hosted_zone_id: ID of the hosted zone in Route53
		record_name: Name of record in a hosted zone. Eg: example.com
		record_type: Record Type of the record.
		new_ttl: New TTL value for a record. Eg: 300

## Lego Input
This Lego takes inputs handle, hosted_zone_id, record_name, record_type, new_ttl

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)