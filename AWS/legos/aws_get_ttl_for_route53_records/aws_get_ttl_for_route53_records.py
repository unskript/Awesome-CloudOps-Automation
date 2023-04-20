##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict, List
import pprint
from unskript.connectors.aws import aws_get_paginator


class InputSchema(BaseModel):
    hosted_zone_id: str = Field(
        ...,
        description='ID of the Hosted zone used for routing traffic.',
        title='Hosted Zone ID',
    )


def aws_get_ttl_for_route53_records_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_get_ttl_for_route53_records(handle, hosted_zone_id:str) -> List:
    """aws_get_ttl_for_route53_records Returns TTL for records in a hosted zone

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :type hosted_zone_id: str
        :param hosted_zone_id: ID of the Hosted zone used for routing traffic.

        :rtype: List of details with the record type, record name and record TTL.
    """
    route53Client = handle.client('route53')
    response = aws_get_paginator(route53Client, "list_resource_record_sets", "ResourceRecordSets", HostedZoneId=hosted_zone_id)
    result = []
    for record in response:
        records = {}
        record_name = record.get('Name')
        record_type = record.get('Type')
        record_ttl = record.get('TTL', 'N/A')
        records["record_name"] = record_name
        records["record_type"] = record_type
        records["record_ttl"] = record_ttl
        result.append(records)
    return result

