[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Get AWS Secret Details</h2>

<br>

## Description
This Action retrieves a Secret from AWS Secret Manager


## Lego Details
    def aws_get_secrets_namager_secret(handle, region: str, secret_name:str) -> str:

        handle: Object of type unSkript datadog Connector
		region: AWS Region
		secret_name: Name of the AWS Secret to obtain

## Lego Input
		region: AWS Region
		secret_name: Name of the AWS Secret to obtain

## Lego Output
Here is a sample output.
<img src="./awsgetsecret.jpg">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)