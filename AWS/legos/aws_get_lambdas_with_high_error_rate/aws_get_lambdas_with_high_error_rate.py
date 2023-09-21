##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Tuple, Optional
import datetime
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions


class InputSchema(BaseModel):
    error_rate_threshold: Optional[float] = Field(
        0.1,
        description='Error rate threshold value. Eg: 0.1 (i.e. 10%)',
        title='Error Rate Threshold',
    )
    days_back: Optional[int] = Field(
        7,
        description=('Number of days to go back. Default value ids 7 days. '
                     'Eg: 7 (This checks for functions with high error rate in the last 7 days)'),
        title='Days Back',
    )
    region: Optional[str] = Field(
        '', 
        description='AWS region. Eg: "us-west-2"',
        title='Region'
    )


def aws_get_lambdas_with_high_error_rate_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_lambdas_with_high_error_rate(
        handle,
        error_rate_threshold:float=0.1,
        days_back:int=7,
        region:str=""
        ) -> Tuple:
    """aws_get_lambdas_with_high_error_rate finds AWS Lambda functions with high error rate

    :type region: string
    :param region: AWS Region to get the instances from. Eg: "us-west-2"

    :type error_rate_threshold: float
    :param error_rate_threshold: (in percent) Idle CPU threshold (in percent)

    :type days_back: int
    :param days_back: (in hours) Idle CPU threshold (in hours)

    :rtype: Tuple with status result and list of Lambda functions with high error rate

    """
    if not handle or (region and region not in aws_list_all_regions(handle)):
        raise ValueError("Invalid input parameters provided.")
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            lambdaClient = handle.client('lambda', region_name=reg)
            cloudwatchClient = handle.client('cloudwatch', region_name=reg)
            # Get a list of all the Lambda functions in your account
            response = lambdaClient.list_functions()
            number_of_days = int(days_back)
            start_time = datetime.datetime.now() - datetime.timedelta(days=number_of_days)
            # Iterate through the list of functions and filter out the ones with a high error rate
            for function in response['Functions']:
                # Get the configuration for the function
                config_response = lambdaClient.get_function_configuration(
                    FunctionName=function['FunctionName']
                    )
                # Get the Errors metric for the function
                errors_response = cloudwatchClient.get_metric_statistics(
                    Namespace='AWS/Lambda',
                    MetricName='Errors',
                    Dimensions=[
                        {
                            'Name': 'FunctionName',
                            'Value': function['FunctionName']
                        },
                    ],
                    StartTime=start_time,
                    EndTime=datetime.datetime.now(),
                    Period=3600,
                    Statistics=['Sum']
                )
                datapoints = errors_response.get('Datapoints')
                if datapoints and 'Sum' in datapoints[0]:
                    errors_sum = datapoints[0]['Sum']
                    invocations = config_response.get('NumberOfInvocations', 0)
                    if invocations > 0:
                        error_rate = errors_sum / invocations
                         # Check if the error rate is greater than the threshold
                        if error_rate > error_rate_threshold:
                            lambda_func = {'function_name': function['FunctionName'], 'region': reg}
                            result.append(lambda_func)
        except Exception:
            pass
    if len(result) != 0:
        return (False, result)
    return (True, None)
