##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.legos.aws.aws_execute_cli_command.aws_execute_cli_command import aws_execute_cli_command
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.connectors.aws import aws_get_paginator
import pprint
import json

class InputSchema(BaseModel):
    region: Optional[str] = Field(
        '', 
        description='AWS region. Eg: "us-west-2"', 
        title='Region'
    )



def aws_find_lambdas_not_using_arm_graviton2_processor_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_find_lambdas_not_using_arm_graviton2_processor(handle,region:str="") -> Tuple:
    """aws_find_lambdas_not_using_arm_graviton2_processor finds AWS Lambda functions wnot using Graviton2 processor

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :type region: string
    :param region: AWS Region to get the instances from. Eg: "us-west-2"

    :rtype: Tuple with status of result and list of Lambda functions that don't use the arm-based graviton2 processor

    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            res = aws_execute_cli_command(handle, f"aws lambda list-functions --region {reg}")
            lambda_functions = json.loads(res)
            for func in lambda_functions['Functions']:
                lambda_details = {}
                if len(lambda_functions['Functions']) != 0:
                    if 'arm64' not in func['Architectures']:
                        lambda_details["lambda_name"] = func['FunctionName']
                        lambda_details["region"] = reg
                        result.append(lambda_details)
        except Exception:
            pass
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)
