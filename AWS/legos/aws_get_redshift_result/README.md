[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Get AWS Redshift Result</h2>

<br>

## Description
This Action retrieves a Result from a Redshift Query. Formats the query into a List for easy manipulation into a dataframe


## Lego Details
    def aws_get_redshift_result(handle, region:str, resultId: str) -> List:

        handle: Object of type unSkript datadog Connector
		region: AWS Region
		resultId: QueryId of teh Redshift Query.

## Lego Input
    handle: Object of type unSkript datadog Connector
	region: AWS Region
	resultId: QueryId of teh Redshift Query.

## Lego Output
Here is a sample output.
<img src="./redshift.jpg">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)