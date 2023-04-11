##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from unskript.enums.aws_route53_record_type_enums import Route53RecordType
from typing import Dict
import pprint

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    hosted_zone_id: str = Field(
        ..., description='ID of the hosted zone in Route53', title='Hosted Zone ID'
    )
    new_ttl: int = Field(
        ..., description='New TTL value for a record. Eg: 300', title='New TTL'
    )
    record_name: str = Field(
        ...,
        description='Name of record in a hosted zone. Eg: example.com',
        title='Record Name',
    )
    record_type: Route53RecordType = Field(
        ..., description='Record Type of the record.', title='Record Type'
    )


def aws_update_ttl_for_route53_records_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_update_ttl_for_route53_records(handle, hosted_zone_id: str, record_name: str, record_type:Route53RecordType, new_ttl:int) -> Dict:
    """aws_update_ttl_for_route53_records updates the TTL for a Route53 record in a hosted zone.

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :type hosted_zone_id: string
        :param hosted_zone_id: ID of the hosted zone in Route53

        :type record_name: string
        :param record_name: Name of record in a hosted zone. Eg: example.com

        :type record_type: string
        :param record_type: Record Type of the record.

        :type new_ttl: int
        :param new_ttl: New TTL value for a record. Eg: 300

        :rtype: Response of updation on new TTL
    """

    route53Client = handle.client('route53')
    new_ttl_value = int(new_ttl)

    response = route53Client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': record_type,
                        'TTL': new_ttl_value
                    }
                }
            ]
        }
    )
    return response

