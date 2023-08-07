##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import pprint
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

    pprint.pprint(output)

def aws_get_schedule_to_retire_instances( handle, region: str="") -> Tuple:
    """aws_get_schedule_to_retire_instances Returns a tuple of instances scheduled to retire.

        :type region: string
        :param region: Used to filter the volume for specific region.

        :rtype: Object with status, list of instances scheduled to retire, and errors
    """
    retiring_instances = {}
    result = []
    all_regions = [region] if region else aws_list_all_regions(handle)

    for r in all_regions:
        try:
            ec2client = handle.client('ec2', region_name=r)
            output = aws_filter_ec2_instances(handle=handle, region=r)
            if output:
                for o in output:
                    all_instances_dict = {"region": r, "instance": o}
                    try:
                        response = ec2client.describe_instance_status(
                            Filters=[{'Name': 'event.code', 'Values': ['instance-retirement']}],
                            InstanceIds=[all_instances_dict['instance']]
                        )
                        instance_statuses = response.get('InstanceStatuses', [])
                        for res in instance_statuses:
                            retiring_instances = {'instance': res['InstanceId'], 'region': r}
                            result.append(retiring_instances)
                    except Exception as e:
                        print(f"An error occurred while describing instance status for instance {o} in region {r}: {e}")
        except Exception:
            pass

    if result:
        return (False, result)
    return (True, None)
