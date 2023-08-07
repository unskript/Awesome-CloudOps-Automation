##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_get_ttl_for_route53_records.aws_get_ttl_for_route53_records import aws_get_ttl_for_route53_records


class InputSchema(BaseModel):
    threshold: Optional[int] = Field(
        default=1,
        description=('(In hours) A threshold in hours to verify route '
                     '53 TTL is within the threshold.'),
        title='Threshold (In hours)',
    )


def aws_get_ttl_under_given_hours_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_ttl_under_given_hours(handle, threshold: int = 1) -> Tuple:
    """aws_get_ttl_under_x_hours Returns TTL for records in a hosted zone

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :type threshold: str
        :param threshold: (In hours) A threshold in hours to verify route
        53 TTL is within the threshold.

        :rtype: List of details with the record type, record name and record TTL.
    """
    if handle is None:
        raise ValueError("Handle must not be None.")

    result = []
    try:
        route_client = handle.client('route53')
        seconds = threshold * 3600
        hosted_zones = aws_get_paginator(route_client, "list_hosted_zones", "HostedZones")
        for zone in hosted_zones:
            zone_id = zone.get('Id')
            if not zone_id:
                continue
            
            record_ttl_data = aws_get_ttl_for_route53_records(handle, zone_id)
            for record_ttl in record_ttl_data:
                if 'record_ttl' not in record_ttl or isinstance(record_ttl['record_ttl'], str):
                    continue
                elif record_ttl['record_ttl'] < seconds:
                    records = {
                        "hosted_zone_id": zone_id,
                        "record_name": record_ttl.get('record_name', ''),
                        "record_type": record_ttl.get('record_type', ''),
                        "record_ttl": record_ttl['record_ttl'],
                    }
                    result.append(records)
    except Exception as e:
        raise e

    if len(result) != 0:
        return (False, result)
    return (True, None)
