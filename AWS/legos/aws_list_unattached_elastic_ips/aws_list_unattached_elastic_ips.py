##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='AWS Region.')


def aws_list_unattached_elastic_ips_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def aws_list_unattached_elastic_ips(handle, region: str = "") -> Tuple:
    """aws_list_unattached_elastic_ips Returns an array of unattached elastic IPs.

        :type region: string
        :param region: AWS Region.

        :rtype: Tuple with status result and list of unattached elastic IPs.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            # Filtering the public_ip by region
            ec2Client = handle.client('ec2', region_name=reg)
            all_eips = ec2Client.describe_addresses()
            for eip in all_eips["Addresses"]:
                vpc_data = {}
                if 'AssociationId' not in eip:
                    vpc_data["public_ip"] = eip['PublicIp']
                    vpc_data["allocation_id"] = eip['AllocationId']
                    vpc_data["region"] = reg
                    result.append(vpc_data)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    return (True, None)
