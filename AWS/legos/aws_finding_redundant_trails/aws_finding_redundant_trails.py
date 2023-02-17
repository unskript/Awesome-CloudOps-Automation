##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Tuple
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint


def aws_finding_redundant_trails_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_finding_redundant_trails(handle) -> Tuple:
    """aws_finding_redundant_trails Returns an array of redundant trails in AWS

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :rtype: Tuple with check status and list of redundant trails
    """
    result = []
    all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            ec2Client = handle.client('cloudtrail', region_name=reg)
            response = ec2Client.describe_trails()
            for glob_service in response["trailList"]:
                trail_dict = {}
                if glob_service["IncludeGlobalServiceEvents"] is True:
                    if len(result) > 0:
                        for i in result:
                            if i["trail_name"] == glob_service["Name"]:
                                i["regions"].append(reg)
                            else:
                                trail_dict["trail_name"] = glob_service["Name"]
                                trail_dict["regions"] = [reg]
                                result.append(trail_dict)
                    else:
                        trail_dict["trail_name"] = glob_service["Name"]
                        trail_dict["regions"] = [reg]
                        result.append(trail_dict)
        except Exception as e:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)