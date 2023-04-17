##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone, timedelta
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        title='Region',
        description='AWS Region.')
    threshold: int = Field(
        default=7,
        title='Threshold(In days)',
        description='The threshold for the reserved instance is scheduled to end within the threshold.')


def aws_get_reserved_instances_about_to_retired_printer(output):
    if output is None:
        return
    pprint.pprint({"Instances": output})


def aws_get_reserved_instances_about_to_retired(handle, region: str = "", threshold: int = 7) -> List:
    """aws_get_reserved_instances_about_to_retired Returns an array of reserved instances.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region to filter instances.
        
        :type threshold: int
        :param threshold: (in days) The threshold for the reserved instance is scheduled to end within the threshold.

        :rtype: Array of instances.
    """
    now = datetime.now(timezone.utc)
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            ec2Client = handle.client('ec2', region_name=reg)
            response = ec2Client.describe_reserved_instances()
            for reserved_id in response["ReservedInstances"]:
                instance_dict = {}
                # check if the Reserved Instance is scheduled to end within the threshold
                if reserved_id['State'] == 'active' and (reserved_id['End'] - now).days <= threshold:
                    instance_dict["instance_id"] = reserved_id["ReservedInstancesId"]
                    instance_dict["region"] = reg
                    result.append(instance_dict)
        except Exception as e:
            pass
        
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)