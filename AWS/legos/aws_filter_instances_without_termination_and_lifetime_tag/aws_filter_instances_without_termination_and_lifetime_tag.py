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

def fetch_instances_from_valid_region(reservations, aws_region, termination_tag_name, lifetime_tag_name):
    result = []
    right_now = date.today()
    
    for reservation in reservations:
        for instance in reservation.get('Instances', []):
            instance_id = instance.get('InstanceId')
            tagged_instance = instance.get('Tags', [])
            
            tag_keys = {tag['Key'] for tag in tagged_instance}
            tag_values = {tag['Key']: tag['Value'] for tag in tagged_instance}

            if not (termination_tag_name in tag_keys and lifetime_tag_name in tag_keys):
                if instance_id:
                    result.append(instance_id)
                continue  # Skip to next instance if tags not found

            try:
                termination_date = datetime.strptime(tag_values.get(termination_tag_name, ''), '%d-%m-%Y').date()
                if termination_date < right_now:
                    result.append(instance_id)

                lifetime_value = tag_values.get(lifetime_tag_name)
                launch_date = datetime.strptime(instance.get('LaunchTime').strftime("%d-%m-%Y"),'%d-%m-%Y').date()
                
                if lifetime_value != 'INDEFINITE' and launch_date < right_now:
                    result.append(instance_id)

            except Exception as e:
                if instance_id:
                    result.append(instance_id)
                print(f"Error processing instance {instance_id}: {e}")

    return {'region': aws_region, 'instances': result} if result else {}

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
    final_list = []
    all_regions = [region] if region else aws_list_all_regions(handle=handle)

    for r in all_regions:
        try:
            ec2Client = handle.client('ec2', region_name=r)
            all_reservations = aws_get_paginator(ec2Client, "describe_instances", "Reservations")
            instances_without_tags = fetch_instances_from_valid_region(all_reservations, r, termination_tag_name, lifetime_tag_name)
            
            if instances_without_tags:
                final_list.append(instances_without_tags)
        except Exception as e:
            pass
    
    if final_list:
        return (False, final_list)
    else:
        return (True, None)