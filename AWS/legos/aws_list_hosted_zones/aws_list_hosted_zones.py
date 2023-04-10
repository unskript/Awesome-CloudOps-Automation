##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List
import pprint
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def aws_list_hosted_zones_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_list_hosted_zones(handle) -> List:
    """aws_list_hosted_zones Returns all hosted zones.

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :rtype: List of all the hosted zones.
    """

    route53Client = handle.client('route53')

    response = route53Client.list_hosted_zones()

    result = []
    for hosted_zone in response['HostedZones']:
        hosted_zone_id = hosted_zone['Id']
        hosted_zone_name = hosted_zone['Name']
        result.append({
            'id': hosted_zone_id,
            'name': hosted_zone_name
        })
    return result


