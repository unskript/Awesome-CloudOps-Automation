from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.legos.utils import CheckOutput, CheckOutputStatus
from unskript.legos.utils import parseARN
from typing import List, Optional, Tuple 
import pprint

class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='Name of the AWS Region'
    )

def aws_list_unhealthy_instances_in_target_group_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def get_all_target_groups(handle, r):
    target_arns_list = []
    elbv2Client = handle.client('elbv2', region_name=r)
    try:
        tbs = aws_get_paginator(elbv2Client, "describe_target_groups", "TargetGroups")
        tbsLength = len(tbs)
        for index, tb in enumerate(tbs):
            target_arns_list.append(tb.get('TargetGroupArn'))
    except Exception as e:
        pass
    return target_arns_list

def aws_list_unhealthy_instances_in_target_group(handle, region: str=None) -> Tuple:
    result = []
    all_target_groups = []
    all_regions = [region]
    if region is None or len(region)==0:
        all_regions = aws_list_all_regions(handle=handle)
    for r in all_regions:
        try:
            output = get_all_target_groups(handle,r)
            if len(output)!=0:
                all_target_groups.append(output)
        except Exception as e:
            pass
    for target_group in all_target_groups:
        for o in target_group:
            parsedArn = parseARN(o)
            elbv2Client = handle.client('elbv2', region_name=parsedArn['region'])
            try:
                targetHealthResponse = elbv2Client.describe_target_health(TargetGroupArn=o)
            except Exception as e:
                return CheckOutput(status=CheckOutputStatus.RUN_EXCEPTION,
                           objects=[],
                           error=e.__str__())
            for ins in targetHealthResponse["TargetHealthDescriptions"]:
                unhealhthy_instances_dict ={}
                if ins['TargetHealth']['State'] in ['unhealthy']:
                    unhealhthy_instances_dict['instance'] = ins['Target']['Id']
                    unhealhthy_instances_dict['region'] = parsedArn['region']
                    result.append(unhealhthy_instances_dict)
    if len(result)!=0:
        return (False, result)
    else:
        return (True, [])