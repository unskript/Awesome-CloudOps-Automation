##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from typing import Tuple, Optional
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.legos.aws.aws_filter_ec2_instances.aws_filter_ec2_instances import aws_filter_ec2_instances


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='Region of the RDS'
    )


def aws_get_schedule_to_retire_instances_printer(output):
    if output is None:
        return
    status, res = output
    if status:
        print("There are no instances that are scheduled to retire.")
    else:
        print(res)

def aws_get_schedule_to_retire_instances( handle, region: str="") -> Tuple:
    """aws_get_schedule_to_retire_instances Returns a tuple of instances scheduled to retire.

        :type region: string
        :param region: Used to filter the volume for specific region.

        :rtype: Object with status, list of instances scheduled to retire, and errors
    """
    result = []
    all_regions = [region] if region or len(region)!=0 else aws_list_all_regions(handle)

    for r in all_regions:
        try:
            ec2client = handle.client('ec2', region_name=r)
            instances = aws_filter_ec2_instances(handle=handle, region=r)
            if not instances:
                print(f"No instances found in {r} region!")
                continue
            try:
                response = ec2client.describe_instance_status(
                    Filters=[{'Name': 'event.code', 'Values': ['instance-retirement']}],
                    InstanceIds=instances
                )
                instance_statuses = response.get('InstanceStatuses', [])
                for res in instance_statuses:
                    result.append({'instance': res['InstanceId'], 'region': r})
            except Exception as e:
                print(f"An error occurred while describing instance status for instances in region {r}: {e}")
        except Exception:
            pass

    return (False, result) if result else (True, None)