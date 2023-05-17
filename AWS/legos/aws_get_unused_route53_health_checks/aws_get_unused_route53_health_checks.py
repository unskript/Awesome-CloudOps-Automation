##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator


class InputSchema(BaseModel):
    hosted_zone_id: Optional[str] = Field(
        default='',
        description='Used to filter the health checks for a specific hosted zone.',
        title='Hosted Zone ID',
    )


def aws_get_unused_route53_health_checks_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def aws_get_unused_route53_health_checks(handle, hosted_zone_id: str = "") -> Tuple:
    """aws_get_unused_route53_health_checks Returns a list of unused Route 53 health checks.

        :type hosted_zone_id: string
        :param hosted_zone_id: Optional. Used to filter the health checks for a specific
        hosted zone.

        :rtype: A tuple containing a list of dicts with information about the unused health checks.
    """
    result = []
    try:
        route_client = handle.client('route53')
        health_checks = aws_get_paginator(route_client, "list_health_checks", "HealthChecks")
        if hosted_zone_id:
            hosted_zones = [{'Id': hosted_zone_id}]
        else:
            hosted_zones = aws_get_paginator(route_client, "list_hosted_zones", "HostedZones")
        used_health_check_ids = set()
        for zone in hosted_zones:
            record_sets = aws_get_paginator(
                route_client,
                "list_resource_record_sets",
                "ResourceRecordSets",
                HostedZoneId=zone['Id']
                )
            for record_set in record_sets:
                if 'HealthCheckId' in record_set:
                    used_health_check_ids.add(record_set['HealthCheckId'])
        for hc in health_checks:
            if hc['Id'] not in used_health_check_ids:
                result.append(hc['Id'])
    except Exception as e:
        raise e

    if len(result) != 0:
        return (False, result)
    return (True, None)
