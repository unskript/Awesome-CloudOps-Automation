[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">]
(https://unskript.com/assets/favicon.png)
<h1>Add Lifecycle Configuration to AWS S3 Bucket</h1>

## Description
Creates a new lifecycle configuration for the bucket or replaces an existing lifecycle configuration.

## Lego Details
	aws_add_lifecycle_configuration_to_s3_bucket(handle, region: str, bucket_name:str, expiration_days:int=30, prefix:str='', noncurrent_days:int=30)
		handle: Object of type unSkript AWS Connector.
		bucket_name: The name of the bucket for which to set the configuration.
		expiration_days: Specifies the expiration for the lifecycle of the object in the form of days. Eg: 30 (days)
		prefix: Prefix identifying one or more objects to which the rule applies.
		noncurrent_days: Specifies the number of days an object is noncurrent before Amazon S3 permanently deletes the noncurrent object versions.


## Lego Input
This Lego takes inputs handle, region, bucket_name, expiration_days, prefix, noncurrent_days.

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)