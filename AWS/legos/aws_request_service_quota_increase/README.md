
[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>AWS Request Service Quota Increase </h1>

## Description
This Action takes a Service and the quota code, along with a requested new quota value, and submits it to AWS for an increase.


## Lego Details

  aws_request_service_quota_increase(handle, service_code:str, quota_code:str, new_quota:float,region:str) -> Dict:

        handle: Object of type unSkript AWS Connector
        service_code: the Service Code (for example EC2)
        Quota_Code: Each quota has a unique code of the form L-XXXXXX.
        region: Location of the S3 buckets.

## Lego Input
This Lego take 4 inputs: handle, service_code, quota_code and region.

## Lego Output
The output shows a HTTP 200 response indicating submission of the request.

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)

