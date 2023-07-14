[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">]
(https://unskript.com/assets/favicon.png)
<h1>AWS Add Tag to Resources</h1>

## Description
For a list of resources, and a tag key/value pair, add the tag to each resource.

## Action Details
	def aws_attach_tags_to_resources(
	    handle,
	    resource_arn: list,
	    tag_key: str,
	    tag_value: str,
	    region: str
	    ) -> Dict:

## Action Input
This Action takes a list of AWS ARNs, and a tag key/value pair, and attached the key value to each ARN.

Note: The AWS API has a limit of 20 ARNs per call, so if you supply >20 ARNs, this Action will split your list into multiple API calls.
	

## Action Output
Here is a sample output.

<img src="./1.png">



## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)