##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from pydantic import BaseModel, Field
from typing import List, Tuple, Optional
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.legos.aws.aws_filter_all_ec2_instances.aws_filter_all_ec2_instances import aws_filter_ec2_instances
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='Region of the RDS'
    )


def aws_get_schedule_to_retire_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_get_schedule_to_retire_instances( handle, region: str=None) ->Tuple:
    """aws_get_schedule_to_retire_instances Returns a tuple of instances scheduled to retire.

        :type region: string
        :param region: Used to filter the volume for specific region.

        :rtype: Tuple with the execution result and list of instances scheduled to retire
    """
    retiring_instances = {} 
    result = [] 
    all_instances = [] 
    all_regions = [region] 
    if region is None or not region:
         all_regions = aws_list_all_regions(handle=handle) 
    try: 
        for r in all_regions: 
            ec2client = handle.client('ec2', region_name=r) 
            output = aws_filter_ec2_instances(handle=handle,region=r)
            if len(output)!=0: 
                for o in output: 
                    all_instances_dict = {} 
                    all_instances_dict["region"]=r 
                    all_instances_dict["instance"]=o 
                    all_instances.append(all_instances_dict) 
    except Exception as error: 
        pass 
    for each_instance in all_instances: 
        try: 
            ec2client = handle.client('ec2', region_name=each_instance['region'])
            response = ec2client.describe_instance_status(Filters=[{'Name': 'event.code','Values': ['instance-retirement']}],InstanceIds=each_instance['instance']) 
            for res in response['InstanceStatuses']: 
                retiring_instances['instance'] = res['InstanceId'] 
                retiring_instances['region'] = each_instance['region'] 
                result.append(retiring_instances) 
        except Exception as error: 
            pass 
    execution_flag = False 
    if len(result) > 0:
        execution_flag = True 
    output = (execution_flag, result) 
    return output
