##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict, List
import pprint

from pydantic import BaseModel, Field


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

    response = route53Client.list_resource_record_sets(HostedZoneId=hosted_zone_id)
    result = []
    for record_set in response['ResourceRecordSets']:
        records = {}
        record_name = record_set['Name']
        record_type = record_set['Type']
        record_ttl = record_set.get('TTL', 'N/A')
        records["record_name"] = record_name
        records["record_type"] = record_type
        records["record_ttl"] = record_ttl
        result.append(records)
    return result

