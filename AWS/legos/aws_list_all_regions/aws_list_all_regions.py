#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#

from pydantic import BaseModel, Field
from typing import Dict, List
import pprint

class InputSchema(BaseModel):
    pass

def aws_list_all_regions_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_list_all_regions(handle) -> List:
    """aws_list_all_regions lists all the AWS regions

        :type handle: object
        :param handle: Object returned from Task Validate

        :rtype: Result List of result
    """

    result = handle.aws_cli_command("aws ec2 describe-regions --all-regions --query 'Regions[].{Name:RegionName}' --output text")
    if result is None or result.returncode != 0:
        print("Error while executing command : {}".format(result))
        return str()
    result_op = list(result.stdout.split("\n"))
    list_region = [x for x in result_op if x != '']
    return list_region