[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>Get list  compute instance by VPC</h1>

## Description
This Lego returns the the list of compute instances filtered by vpc.

## Lego Details

    gcp_list_instances_by_vpc(handle: object, project: str, zone: str, vpc_id: str)

        handle: Object of type unSkript GCP Connector
        project: String GCP Project name
        zone: String, Zone in which to get the instnances list from
        vpc_id: Name of the VPC.


## Lego Input
 project:  GCP Project name eg. "acme-dev"
 zone: GCP Zone eg. "us-west1-b"
 vpc_id: Name of the VPC.

## Lego Output
Here is a sample output.

<img src="./1.png">



## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)
