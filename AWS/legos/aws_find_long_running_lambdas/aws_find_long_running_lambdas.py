##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Tuple, Optional
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint
import datetime


class InputSchema(BaseModel):
    days_back: Optional[int] = Field(
        default=7,
        title="Days to Search",
        description="(In days) An integer specifying the number of days to search back for logs.")
    duration_threshold: Optional[int] = Field(
        default=500,
        title="Minimum Duration of a Lambda Function",
        description="(In milliseconds) specifying the threshold for the minimum runtime of a Lambda function.")
    region: Optional[str] = Field(
        title='Region',
        description='AWS Region')


def aws_find_long_running_lambdas_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_find_long_running_lambdas(handle, days_back: int = 7, duration_threshold: int = 500, region: str = "") -> Tuple:
    """aws_find_long_running_lambdas Returns an List long running lambdas.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: str
        :param region: AWS Region.

        :type days_back: int
        :param days_back: (In days) An integer specifying the number of days to search back for logs.
        
        :type duration_threshold: int
        :param duration_threshold: (In milliseconds) specifying the threshold for the minimum runtime of a Lambda function.

        :rtype: List long running lambdas.
    """
    result = []
    start_time = datetime.datetime.now() - datetime.timedelta(days=days_back)
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            lambda_client = handle.client('lambda', region_name=reg)
            log_client = handle.client('logs', region_name=reg)
            response = aws_get_paginator(lambda_client, "list_functions", "Functions")
            for function in response:
                function_name = function['FunctionName']
                log_group_name = f"/aws/lambda/{function_name}"
                try:
                    # Call the FilterLogEvents method to search the logs for the function
                    log_response = aws_get_paginator(log_client, "filter_log_events", "events",
                                                     logGroupName=log_group_name,
                                                     startTime=int(start_time.timestamp() * 1000))
                    for event in log_response:
                        if 'REPORT' in event['message']:
                            message_data = event['message'].split('\t')
                            duration_index = message_data.index('Duration:') + 1
                            duration_str = message_data[duration_index].strip()
                            duration = float(duration_str[:-2])
                            if duration >= duration_threshold:
                                result.append({'function_name': function_name, 'duration': duration, "region": reg})
                except:
                    pass
        except Exception as error:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)