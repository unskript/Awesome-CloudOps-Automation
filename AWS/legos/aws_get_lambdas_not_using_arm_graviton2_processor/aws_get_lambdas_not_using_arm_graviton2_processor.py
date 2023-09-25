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


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        '', 
        description='AWS region. Eg: "us-west-2"', 
        title='Region'
    )



def aws_get_lambdas_not_using_arm_graviton2_processor_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_lambdas_not_using_arm_graviton2_processor(handle, region: str = "") -> Tuple:
    """aws_get_lambdas_not_using_arm_graviton2_processor finds AWS Lambda functions wnot using Graviton2 processor

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :type region: string
    :param region: AWS Region to get the instances from. Eg: "us-west-2"

    :rtype: Tuple with status of result and list of Lambda functions that don't use the arm-based graviton2 processor
    """

    result = []
    all_regions = [region] if region else aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            lambda_client = handle.client('lambda', region_name=reg)
            response = aws_get_paginator(lambda_client, "list_functions", "Functions")
            for res in response:
                architectures = res.get('Architectures', [])
                function_name = res.get('FunctionName', "")
                if 'arm64' not in architectures and function_name:
                    result.append({"function_name": function_name, "region": reg})
        except Exception as e:
            pass

    if result:
        return (False, result)
    return (True, None)