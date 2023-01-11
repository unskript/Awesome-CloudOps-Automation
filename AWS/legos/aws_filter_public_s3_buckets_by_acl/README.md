[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>Get AWS public S3 Buckets by ACL</h1>

## Description
This Lego Get AWS public S3 Buckets.


## Lego Details

    aws_get_public_s3_buckets(handle: object, permission:Enum, region: str)

        handle: Object of type unSkript AWS Connector.
        permission: Enum, Set of permissions that AWS S3 supports in an ACL for buckets and objects. Eg: "READ","WRITE_ACP","FULL_CONTROL"
        region: region: Optional, AWS region. Eg: “us-west-2”

## Lego Input
This Lego takes three inputs handle, permission, region.

## Lego Output
Here is a sample output.
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)