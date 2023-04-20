
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field



##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##

#here is a sample quota input:
#[{'QuotaName':'VPCs Per Region','ServiceCode':'vpc',
#    'QuotaCode': 'L-F678F1CE', 'ApiName': 'describe_vpcs', 
#      'ApiFilter' : '[]','ApiParam': 'Vpcs', 'initialQuery': ''}]
# the values are described in a blog post: 
# https://unskript.com/aws-service-quotas-discovering-where-you-stand/

class InputSchema(BaseModel):
    region: str = Field(..., description='AWS Region of the instances.', title='Region')
    warning_percentage: float = Field(
        50,
        description='Threshold for alerting Service Quota. If set to 50, any service at 50% of quota usage will be reported.',
        title='warning_percentage',
    )
    quota_input: List = Field(
        '', description='Array of inputs - see readme for format', title='quota_input'
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
def aws_service_quota_limits_printer(output):
    if output is None:
        return
    pprint.pprint({"Instances": output})


@beartype
@beartype
def aws_service_quota_limits(handle, region: str, warning_percentage: float, quota_input: List) -> List:

    sqClient = handle.client('service-quotas',region_name=region)
    ec2Client = handle.client('ec2', region_name=region)

    result = []

    for i in quota_input:   
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
                #sample exception to the else rule
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

                #rebuild filter
                #print("test", j[initialQueryFilter])
                variableReplace = j[initialQueryFilter]
                filterList = i.get('ApiFilter')
                filterList = filterList.replace("VARIABLE", variableReplace)
                filterList = json.loads(filterList)

                res2 = aws_get_paginator(ec2Client, i.get('ApiName'), i.get('ApiParam'), Filters=filterList)

                #most of the time we can just count the length of the response (else)
                if i.get('QuotaName') =="Participant accounts per VPC":
                        print("this is an exception, and you'll ahve to write custom code here")
                else:
                    count = len(res2)

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



