##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import List, Optional
from pydantic import BaseModel, Field
import pprint
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.legos.aws.aws_get_all_ec2_instances.aws_get_all_ec2_instances import aws_get_all_ec2_instances


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        '', description='AWS Region to get the RDS Instance', title='AWS Region'
    )
    instance_ids: Optional[List] = Field(
        '', description='List of instance IDs to check.', title='List of Instance IDs'
    )
    threshold: Optional[float] = Field(
        default= 2,
        description='The CPU size threshold. Default value is 2.0. Size map is as follows-\n    "nano": 2,\n    "micro": 2,\n    "small": 1,\n    "medium": 1,\n    "large": 2,\n    "xlarge": 4,\n    "2xlarge": 8,\n    "3xlarge": 12,\n    "4xlarge": 16,\n    "6xlarge": 24,\n    "8xlarge": 32,\n    "9xlarge": 36,\n    "10xlarge": 40,\n    "12xlarge": 48,\n    "16xlarge": 64,\n    "18xlarge": 72,\n    "24xlarge": 96,\n    "32xlarge": 128,\n    "metal": 96',
        title='Threshold (vCPU)',
    )


def aws_get_ec2_instances_with_smaller_cpu_size_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_get_ec2_instances_with_smaller_cpu_size(handle, instance_ids: list = [], region: str = "", threshold: float=2.0):
    """Check the CPU size (vCPU count) and compare with the threshold.

    :type threshold: float
    :param threshold: The CPU size threshold. Example value is 2.0.

    :type instance_ids: list
    :param instance_ids: List of instance IDs to check.

    :type region: str
    :param region: Region to get instances from.

    :rtype: Status, List of dicts of instance IDs with CPU size less than the threshold
    """
    size_to_cpu_map = {
    "nano": 2,
    "micro": 2,
    "small": 1,
    "medium": 1,
    "large": 2,
    "xlarge": 4,
    "2xlarge": 8,
    "3xlarge": 12,
    "4xlarge": 16,
    "6xlarge": 24,
    "8xlarge": 32,
    "9xlarge": 36,
    "10xlarge": 40,
    "12xlarge": 48,
    "16xlarge": 64,
    "18xlarge": 72,
    "24xlarge": 96,
    "32xlarge": 128,
    "metal": 96
    }
    result = []
    instances_with_low_cpu_size = {}

    try:
        if instance_ids and not region:
            raise SystemError("Region must be specified when instance IDs are given.")

        if instance_ids and region:
            # If instance_ids and region are given
            regions = [region]
            all_instance_ids = [{region: instance_ids}]
        elif not instance_ids and region:
            # If instance_ids are not given but region is given
            regions = [region]
            all_instance_ids = [{region: aws_get_all_ec2_instances(handle, region)}]
        else:
            # If neither instance_ids nor region are given
            regions = aws_list_all_regions(handle)
            all_instance_ids = []
            for region in regions:
                try:
                    all_instance_ids.append({region:aws_get_all_ec2_instances(handle, region)})
                except Exception:
                    pass

        for region_instances in all_instance_ids:
            for region, instance_ids in region_instances.items():
                ec2 = handle.client('ec2', region_name=region)
                for instance_id in instance_ids:
                    # Get the instance details
                    resp = ec2.describe_instances(InstanceIds=[instance_id])
                    # Get the instance type
                    instance_type = resp['Reservations'][0]['Instances'][0]['InstanceType']
                    # Get the size from the instance type
                    instance_size = instance_type.split('.')[1]
                    # Get the vCPU count from the size using the mapping
                    cpu_size = size_to_cpu_map.get(instance_size, 0)

                    # If the CPU size is less than the threshold, add to the list.
                    if cpu_size < threshold:
                        if region not in instances_with_low_cpu_size:
                            instances_with_low_cpu_size = {"region":region, "instance_id": instance_id}
                            result.append(instances_with_low_cpu_size)

    except Exception as e:
        raise e

    if len(result) != 0:
        return (False, result)
    return (True, None)


