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
    termination_tag_name: Optional[str] = Field(
        default="terminationDateTag",
        title='Termination Date Tag Name',
        description='Name of the Termination Date Tag given to an EC2 instance. By default "terminationDateTag" is considered '
    )
    lifetime_tag_name: Optional[str] = Field(
        default="lifetimeTag",
        title='Lifetime Tag Name',
        description='Name of the Lifetime Date Tag given to an EC2 instance. By default "lifetimeTag" is considered '
    )


def aws_filter_instances_without_termination_and_lifetime_tag_printer(output):
    if output is None:
        return
    
    pprint.pprint(output)

def fetch_instances_from_valid_region(res,r, termination_tag_name, lifetime_tag_name):
    result = []
    right_now = date.today()
    for reservation in res:
        for instance in reservation['Instances']:
            try:
                if 'Tags' in instance:
                    tagged_instance = instance['Tags']
                    tag_keys = [tags['Key'] for tags in tagged_instance]

                    if termination_tag_name not in tag_keys or lifetime_tag_name not in tag_keys:
                        if 'InstanceId' in instance:
                            result.append(instance['InstanceId'])
                        continue  # Skip to next instance if tags not found

                    for x in instance['Tags']:
                        if x['Key'] == termination_tag_name:
                            date_object = datetime.strptime(x['Value'], '%d-%m-%Y').date()
                            if date_object < right_now:
                                result.append(instance['InstanceId'])

                        elif x['Key'] == lifetime_tag_name:
                            launch_time = instance['LaunchTime']
                            convert_to_datetime = launch_time.strftime("%d-%m-%Y")
                            launch_date = datetime.strptime(convert_to_datetime,'%d-%m-%Y').date()
                            if x['Value'] != 'INDEFINITE' and launch_date < right_now:
                                result.append(instance['InstanceId'])

                else:
                    if 'InstanceId' in instance:
                        result.append(instance['InstanceId'])

            except Exception as e:
                if 'InstanceId' in instance:
                    result.append(instance['InstanceId'])
                print(f"Error processing instance {instance['InstanceId']}: {e}")

    instances_dict = {'region': r, 'instances': result} if result else {}
    return instances_dict
    
def aws_filter_instances_without_termination_and_lifetime_tag(handle, region: str=None, termination_tag_name:str='terminationDateTag', lifetime_tag_name:str='lifetimeTag') -> Tuple:
    """aws_filter_ec2_without_lifetime_tag Returns an List of instances which not have lifetime tag.

        Assumed tag key format - terminationDateTag, lifetimeTag
        Assumed Date format for both keys is -> dd-mm-yy

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Optional, Name of AWS Region

        :type termination_tag_name: string
        :param termination_tag_name: Optional, Name of the Termination Date Tag given to an EC2 instance. By default "terminationDateTag" is considered 

        :type lifetime_tag_name: string
        :param lifetime_tag_name: Optional, Name of the Lifetime Date Tag given to an EC2 instance. By default "lifetimeTag" is considered 

        :rtype: Tuple of status, instances which dont having terminationDateTag and lifetimeTag, and error
    """
    final_list=[]
    all_regions = [region]
    if region is None or len(region) == 0:
        all_regions = aws_list_all_regions(handle=handle)
    for r in all_regions:
        try:
            ec2Client = handle.client('ec2', region_name=r)
            all_reservations = aws_get_paginator(ec2Client, "describe_instances", "Reservations")
            instances_without_tags = fetch_instances_from_valid_region(all_reservations, r, termination_tag_name, lifetime_tag_name)
            if len(instances_without_tags)!=0:
                final_list.append(instances_without_tags)
        except Exception as e:
            pass
    if len(final_list)!=0:
        return (False, final_list)
    else:
        return (True, None)
