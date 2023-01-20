##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List, Tuple, Optional
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint
from datetime import datetime, date

class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='Name of the AWS Region'
    )


def aws_filter_instances_without_termination_and_lifetime_tag_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def fetch_instances_from_valid_region(res,r):
    result=[]
    instances_dict={}
    for reservation in res:
            for instance in reservation['Instances']:
                try:
                    tagged_instance = instance['Tags']
                    tag_keys = [tags['Key'] for tags in tagged_instance]
                    if 'terminationDateTag' not in tag_keys or 'lifetimeTag' not in tag_keys:
                        result.append(instance['InstanceId'])
                    elif 'terminationDateTag' not in tag_keys and 'lifetimeTag' not in tag_keys:
                        result.append(instance['InstanceId'])
                    if 'terminationDateTag' in tag_keys:
                        for x in instance['Tags']:
                            if x['Key'] == 'terminationDateTag':
                                right_now = date.today()
                                date_object = datetime.strptime(x['Value'], '%d-%m-%Y').date()
                                if date_object < right_now:
                                    result.append(instance['InstanceId'])
                            elif x['Key'] == 'lifetimeTag':
                                launch_time = instance['LaunchTime']
                                convert_to_datetime = launch_time.strftime("%d-%m-%Y")
                                launch_date = datetime.strptime(convert_to_datetime,'%d-%m-%Y').date()
                                if x['Value'] is not 'INDEFINITE':
                                    if launch_date < right_now:
                                        result.append(instance['InstanceId'])
                except Exception as e:
                        if len(instance['InstanceId'])!=0:
                            result.append(instance['InstanceId'])
    if len(result)!=0:
        instances_dict['region']= r
        instances_dict['instances']= result
    return instances_dict

def aws_filter_instances_without_termination_and_lifetime_tag(handle, region: str=None) -> Tuple:
    """aws_filter_ec2_without_lifetime_tag Returns an List of instances which not have lifetime tag.

        Assumed tag key format - terminationDateTag, lifetimeTag
        Assumed Date format for both keys is - dd-mm-yy

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Used to filter the instance for specific region.

        :rtype: Tuple of result and instances which dont having terminationDateTag and lifetimeTag
    """
    final_list=[]
    all_regions = [region]
    if region is None or len(region) == 0:
        all_regions = aws_list_all_regions(handle=handle)
    for r in all_regions:
        try:
            ec2Client = handle.client('ec2', region_name=r)
            all_reservations = aws_get_paginator(ec2Client, "describe_instances", "Reservations")
            instances_without_tags = fetch_instances_from_valid_region(all_reservations,r)
            if len(instances_without_tags)!=0:
                final_list.append(instances_without_tags)
        except Exception as e:
            pass
    execution_flag = False
    if len(final_list) > 0:
        execution_flag = True
    output = (execution_flag, final_list)
    return output

