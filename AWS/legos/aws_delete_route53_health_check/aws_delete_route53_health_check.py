##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict
import pprint


class InputSchema(BaseModel):
    health_check_id: str = Field(
        title='Health Check ID',
        description='The ID of the Health Check to delete.')


def aws_delete_route53_health_check_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_delete_route53_health_check(handle, health_check_id: str) -> Dict:
    """aws_delete_route53_health_check Deletes a Route 53 Health Check.

        :type health_check_id: string
        :param health_check_id: The ID of the Health Check to delete.

        :rtype: dict of health check information.
    """
    try:
        route_client = handle.client('route53')
        response = route_client.delete_health_check(HealthCheckId=health_check_id)
        return response
    except Exception as e:
        raise Exception(e)