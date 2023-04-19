
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field



##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##

class InputSchema(BaseModel):
    region: str = Field(..., description='AWS Region.', title='Region')
    warning_percentage: float = Field(
        50,
        description='Percentage threshold for a warning.  For a complete list of quotas, use 0.',
        title='warning_percentage',
    )



from pydantic import BaseModel, Field
from typing import List
from unskript.connectors.aws import aws_get_paginator
import pprint
import json
import datetime

from beartype import beartype

from beartype import beartype
@beartype
def aws_service_quota_limits_vpc_printer(output):
    if output is None:
        return
    pprint.pprint({"Instances": output})


@beartype
@beartype
def aws_service_quota_limits_vpc(handle, region: str, warning_percentage: float) -> List:


    ## EC@ and VPCs

    ec2Client = handle.client('ec2', region_name=region)
    # List all VPCs in the specified region

    q_table = [ 
        #per region stats
                #per region stats
        {'QuotaName':'VPCs Per Region','ServiceCode':'vpc','QuotaCode': 'L-F678F1CE', 'ApiName': 'describe_vpcs', 'ApiFilter' : '[]','ApiParam': 'Vpcs', 'initialQuery': ''},
        {'QuotaName':'VPC security groups per Region','ServiceCode':'vpc','QuotaCode': 'L-E79EC296','ApiName': 'describe_security_groups', 'ApiFilter' :'[]','ApiParam': 'SecurityGroups', 'initialQuery': ''},
        {'QuotaName':'Egress-only internet gateways per Region','ServiceCode':'vpc','QuotaCode': 'L-45FE3B85','ApiName': 'describe_egress_only_internet_gateways', 'ApiFilter' : '[]','ApiParam': 'EgressOnlyInternetGateways', 'initialQuery': ''},
        {'QuotaName':'Gateway VPC endpoints per Region','ServiceCode':'vpc','QuotaCode': 'L-1B52E74A','ApiName': 'describe_vpc_endpoints', 'ApiFilter' : '[{"Name": "vpc-endpoint-type","Values": ["Gateway"]}]','ApiParam': 'VpcEndpoints', 'initialQuery': ''},
        {'QuotaName':'Internet gateways per Region','ServiceCode':'vpc','QuotaCode': 'L-A4707A72','ApiName': 'describe_internet_gateways', 'ApiFilter' : '[]','ApiParam': 'InternetGateways', 'initialQuery': ''},
        {'QuotaName':'Network interfaces per Region','ServiceCode':'vpc','QuotaCode': 'L-DF5E4CA3','ApiName': 'describe_network_interfaces', 'ApiFilter' : '[]','ApiParam': 'NetworkInterfaces', 'initialQuery': ''},
        #per VPC stats
        {'QuotaName':'Active VPC peering connections per VPC',
         'ServiceCode':'vpc',
         'QuotaCode': 'L-7E9ECCDB',
         'ApiName': 'describe_vpc_peering_connections', 
         'ApiFilter' : '[{"Name": "status-code","Values": ["active"]}, {"Name": "requester-vpc-info.vpc-id","Values": ["VARIABLE"]}]',
         'ApiParam': 'VpcPeeringConnections', 
         'initialQuery': '["describe_vpcs","Vpcs", "VpcId"]'},
        {'QuotaName':'Interface VPC endpoints per VPC',
         'ServiceCode':'vpc',
         'QuotaCode': 'L-29B6F2EB',
         'ApiName': 'describe_vpc_endpoints', 
         'ApiFilter' : '[{"Name": "vpc-endpoint-type","Values": ["Interface"]}, {"Name": "vpc-id","Values": ["VARIABLE"]}]',
         'ApiParam': 'VpcEndpoints', 
         'initialQuery': '["describe_vpcs","Vpcs", "VpcId"]'},
        {'QuotaName':'IPv4 CIDR blocks per VPC',
         'ServiceCode':'vpc',
         'QuotaCode': 'L-83CA0A9D',
         'ApiName': '', 
         'ApiFilter': '',
         'ApiParam': 'CidrBlockAssociationSet', 
         'initialQuery': '["describe_vpcs","Vpcs", "VpcId"]'},
        {'QuotaName':' Network ACLs per VPC',
         'ServiceCode':'vpc',
         'QuotaCode': 'L-B4A6D682',
         'ApiName': 'describe_network_acls', 
         'ApiFilter': '[{"Name": "vpc-id","Values": ["VARIABLE"]}]',
         'ApiParam': 'NetworkAcls', 
         'initialQuery': '["describe_vpcs","Vpcs", "VpcId"]'},
        {'QuotaName':'Participant accounts per VPC',
         'ServiceCode':'vpc',
         'QuotaCode': 'L-2C462E13',
         'ApiName': 'describe_vpc_peering_connections', 
         'ApiFilter': '[{"Name": "requester-vpc-info.vpc-id","Values": ["VARIABLE"]}]',
         'ApiParam': 'VpcPeeringConnections', 
         'initialQuery': '["describe_vpcs","Vpcs", "VpcId"]'},
        {'QuotaName':'Route tables per VPC',
         'ServiceCode':'vpc',
         'QuotaCode': 'L-589F43AA',
         'ApiName': 'describe_route_tables', 
         'ApiFilter': '[{"Name": "vpc-id","Values": ["VARIABLE"]}]',
         'ApiParam': 'RouteTables', 
         'initialQuery': '["describe_vpcs","Vpcs", "VpcId"]'},
        {'QuotaName':'Subnets per VPC',
         'ServiceCode':'vpc',
         'QuotaCode': 'L-407747CB',
         'ApiName': 'describe_subnets', 
         'ApiFilter': '[{"Name": "vpc-id","Values": ["VARIABLE"]}]',
         'ApiParam': 'Subnets', 
         'initialQuery': '["describe_vpcs","Vpcs", "VpcId"]'},
        {'QuotaName':'NAT gateways per Availability Zone',
          'ServiceCode':'vpc',
          'QuotaCode': 'L-FE5A380F',
          'ApiName': 'describe_nat_gateways', 
          'ApiFilter': '[]',
          'ApiParam': 'NatGateways', 
          'initialQuery': ''},
        {'QuotaName':'Inbound or outbound rules per security group',
          'ServiceCode':'vpc',
          'QuotaCode': 'L-0EA8095F',
          'ApiName': 'describe_security_groups', 
          'ApiFilter': '[]',
          'ApiParam': 'SecurityGroups', 
          'initialQuery': ''},
        {'QuotaName':'Outstanding VPC peering connection requests',
         'ServiceCode':'vpc',
         'QuotaCode': 'L-DC9F7029',
         'ApiName': 'describe_vpc_peering_connections', 
         'ApiFilter': '[{"Name": "status-code", "Values": ["pending-acceptance"]}]',
         'ApiParam': 'VpcPeeringConnections', 
         'initialQuery': ''},
        {'QuotaName':'Routes per route table',
         'ServiceCode':'vpc',
         'QuotaCode': 'L-93826ACB',
         'ApiName': 'describe_route_tables', 
         'ApiFilter': '[]',
         'ApiParam': 'RouteTables', 
         'initialQuery': ''},
        {'QuotaName':'Rules per network ACL',
         'ServiceCode':'vpc',
         'QuotaCode': 'L-2AEEBF1A',
         'ApiName': 'describe_network_acls', 
         'ApiFilter': '[]',
         'ApiParam': 'NetworkAcls', 
         'initialQuery': ''},
        {'QuotaName':'Security groups per network interface',
         'ServiceCode':'vpc',
         'QuotaCode': 'L-2AFB9258',
         'ApiName': 'describe_network_interfaces', 
         'ApiFilter': '[]',
         'ApiParam': 'NetworkInterfaces', 
         'initialQuery': ''},
        {'QuotaName':'VPC peering connection request expiry hours',
         'ServiceCode':'vpc',
         'QuotaCode': 'L-8312C5BB',
         'ApiName': 'describe_vpc_peering_connections', 
         'ApiFilter': '[{"Name": "expiration-time"}]',
         'ApiParam': 'VpcPeeringConnections', 
         'initialQuery': ''}
    ]
    #print(q_table)
    result = []

    sqClient = handle.client('service-quotas',region_name=region)
    for i in q_table:   
        #convert the ApiFilter to a list
        #'[{"Name": "vpc-endpoint-type","Values": ["Gateway"]}]'
        filterList=''
        if len(i.get('ApiFilter')) > 0:
            filterList = json.loads(i.get('ApiFilter'))
        #print("filter", filterList)

        #get quota
        sq = sqClient.get_service_quota(
            ServiceCode=i.get('ServiceCode'),
            QuotaCode=i.get('QuotaCode'))
        quotaValue =sq['Quota']['Value']

        #simple queries (Only one call to get the details)
        if i.get('initialQuery') == '':
            #find usage
            res = aws_get_paginator(ec2Client, i.get('ApiName'), i.get('ApiParam'), Filters=filterList)

            #most of the time, all we need is the length (else)
            if i.get('QuotaName')=="NAT gateways per Availability Zone":
                #count the subets per nat gateway
                # Create a dictionary to store the count of NAT gateways for each Availability Zone
                az_nat_gateway_count = {}
                # Loop through each NAT gateway and count the number for each Availability Zone
                for nat_gateway in res:
                    az = nat_gateway['SubnetId']
                    if az in az_nat_gateway_count:
                        az_nat_gateway_count[az] += 1
                    else:
                        az_nat_gateway_count[az] = 1

                for gw in az_nat_gateway_count:
                    percentage = az_nat_gateway_count[gw]/quotaValue
                    combinedData = {'Quota Name': i.get('QuotaName') + ": "+ gw , 'Limit':quotaValue, 'used': az_nat_gateway_count[gw], 'percentage':percentage}
                    result.append( combinedData)
                    #print(combinedData)
            if i.get('QuotaName')=="Inbound or outbound rules per security group":
                for security_group in res:
                    ruleCount = len(security_group['IpPermissions']) +len(security_group['IpPermissionsEgress'])
                    percentage = ruleCount/quotaValue
                    if len(i.get('QuotaName'))>0:
                        combinedData = {'Quota Name': i.get('QuotaName') +": "+ security_group['GroupName'] , 'Limit':quotaValue, 'used': ruleCount, 'percentage':percentage}
                        result.append(combinedData)
                        #print(combinedData)
            if i.get('QuotaName')=="Routes per route table":
                for route_table in res:
                    route_count = len(route_table['Routes'])
                    route_table_id = route_table['RouteTableId']
                    percentage = route_count/quotaValue
                    combinedData = {'Quota Name': i.get('QuotaName') +": "+ route_table_id , 'Limit':quotaValue, 'used': route_count, 'percentage':percentage}
                    result.append(  combinedData)
                    #print(combinedData)
            if i.get('QuotaName')=="Rules per network ACL":
                for network_acl in res:
                    rule_count = len(network_acl['Entries'])
                    network_acl_id = network_acl['NetworkAclId']
                    percentage = rule_count/quotaValue
                    combinedData = {'Quota Name': i.get('QuotaName') +": "+ network_acl_id , 'Limit':quotaValue, 'used': rule_count, 'percentage':percentage}
                    result.append(  combinedData)
                    #print(combinedData)
            if i.get('QuotaName')=="Security groups per network interface":
                for network_interface in res:
                    security_group_count = len(network_interface['Groups'])
                    network_interface_id = network_interface['NetworkInterfaceId']
                    percentage = security_group_count/quotaValue
                    if len(i.get('QuotaName'))>0:
                        combinedData = {'Quota Name': i.get('QuotaName') +": "+ network_interface_id , 'Limit':quotaValue, 'used': security_group_count, 'percentage':percentage}
                        result.append(combinedData)
                        #print(combinedData)
            if i.get('QuotaName')=="VPC peering connection request expiry hours":
                if len(res)>0:
                    for peering_connection in res:
                        expiration_time = peering_connection['ExpirationTime']
                        current_time = datetime.now(datetime.timezone.utc)
                        time_remaining = expiration_time - current_time
                        peering_connection_id = peering_connection['VpcPeeringConnectionId']
                        percentage = time_remaining/quotaValue
                        combinedData = {'Quota Name': i.get('QuotaName') +": "+ peering_connection_id , 'Limit':quotaValue, 'used': time_remaining, 'percentage':percentage}
                        result.append(combinedData)
                        #print(combinedData)
            else:
                #most common default case
                count = len(res)
                percentage = count/quotaValue
                combinedData = {'Quota Name': i.get('QuotaName'), 'Limit':quotaValue, 'used': count, 'percentage':percentage}
                result.append(  combinedData)
                #print(combinedData)

        #nested queries (get X per VPC or get y per network interface)
        else:
            #nested query for quota
            #for example 'initialQuery': ['describe_vpcs','Vpcs', 'VpcId'] gets the list of VPCs, that we can then ask abour each VPC
            #turn initalQuery string into a list
            #'initialQuery': ['describe_vpcs','Vpcs', 'VpcId']
            initialQuery = json.loads(i.get('initialQuery'))
            initialQueryName = initialQuery[0]
            initialQueryParam  = initialQuery[1]
            initialQueryFilter = initialQuery[2]

            #inital Query
            res = aws_get_paginator(ec2Client, initialQueryName, initialQueryParam)
            #print(res)
            #nested query
            for j in res:

                #most of the time, there will be a 2nd query, and the table will have an 'ApiName' value
                if len(i.get('ApiName')) >0:
                    #rebuild filter
                    #print("test", j[initialQueryFilter])
                    variableReplace = j[initialQueryFilter]
                    filterList = i.get('ApiFilter')
                    filterList = filterList.replace("VARIABLE", variableReplace)
                    filterList = json.loads(filterList)

                    res2 = aws_get_paginator(ec2Client, i.get('ApiName'), i.get('ApiParam'), Filters=filterList)

                    #most of the time we can just count the length of the response (else)
                    if i.get('QuotaName') =="Participant accounts per VPC":
                        count =0
                        #there can be zero peering conncetions....
                        if len(res2) >0:
                            for connection in res2:
                                if len(connection['AccepterVpcInfo']['OwnerId']) >0:
                                    count += 1
                    else:
                        count = len(res2)
                else:
                    #the value is in the first query, but we need to loop through it
                    apiParam = i.get('ApiParam')    
                    #print(apiParam, j[apiParam])
                    count = len(j[apiParam])
                percentage = count/quotaValue
                objectResult = {j[initialQueryFilter] : count}
                #print(objectResult)
                quotaName = f"{i.get('QuotaName')} for {j[initialQueryFilter]}"
                combinedData = {'Quota Name': quotaName, 'Limit':quotaValue, 'used': count, 'percentage':percentage}
                result.append(combinedData)
                #print(combinedData)


    # all the data is now in a list called result
    warning_result =[]
    threshold = warning_percentage/100
    for quota in result:
        if quota['percentage'] >= threshold:
            #there are two sums that appear, and throw errors.
            if quota['Quota Name'] != 'Inbound or outbound rules per security group':
                if quota['Quota Name'] != 'Security groups per network interface':
                    warning_result.append(quota)
    return warning_result



