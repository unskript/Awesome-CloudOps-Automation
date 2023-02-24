[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>AWS Service Quota Limits </h1>

## Description
This Action compares usage for all input service quotas vs. your account's limit.  If any are above warning percentage - they will be output.


## Lego Details

    def aws_service_quota_limits_vpc(handle, region: str, warning_percentage: float, quota_input: List) -> List:

        handle: Object of type unSkript AWS Connector
        warning_percentage: If % is above this value - the service will be output.
        region: Region for instance.
        quota_input: List of Quota data. The format is described in this blog post: https://unskript.com/aws-service-quotas-discovering-where-you-stand/

       Sample quota input:
       [{'QuotaName':'VPCs Per Region','ServiceCode':'vpc',
            'QuotaCode': 'L-F678F1CE', 'ApiName': 'describe_vpcs', 
            'ApiFilter' : '[]','ApiParam': 'Vpcs', 'initialQuery': ''}]

## Lego Input
This Lego take fout inputs handle, region, quota_input and warning_percentage.

## Lego Output
Here is a sample output.

<img src="./1.jpg">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)