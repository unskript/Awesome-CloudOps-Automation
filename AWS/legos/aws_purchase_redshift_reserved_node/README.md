[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">]
(https://unskript.com/assets/favicon.png)
<h1>AWS Purchase Redshift Reserved Nodes</h1>

## Description
This action purchases reserved nodes. Amazon Redshift offers a predefined set of reserved node offerings. You can purchase one or more of the offerings.

## Lego Details
	aws_purchase_redshift_reserved_node(handle, region: str, reserved_node_offering_id: str, no_of_nodes:int=1)
		handle: Object of type unSkript AWS Connector.
		no_of_nodes: The number of reserved nodes that you want to purchase.
		reserved_node_offering_id: The unique identifier of the reserved node offering you want to purchase. Example: '438012d3-4052-4cc7-b2e3-8d3372e0e706'

## Lego Input
This Lego takes inputs handle, no_of_nodes, reserved_node_offering_id.

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)