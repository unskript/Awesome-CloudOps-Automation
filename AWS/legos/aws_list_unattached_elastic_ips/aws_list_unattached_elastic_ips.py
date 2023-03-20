##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint


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
            ec2Client = handle.resource('ec2', region_name=reg)
            all_eips = ec2Client.vpc_addresses.all()
            for eip in all_eips:
                vpc_data = {}
                if not eip.instance_id and not eip.network_interface_id:
                    vpc_data["public_ip"] = eip.public_ip
                    vpc_data["region"] = reg
        except Exception as e:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)
