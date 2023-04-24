##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Tuple
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint
import datetime
from typing import Optional

class InputSchema(BaseModel):
    days_back: Optional[int] = Field(
        1,
        description='(in days) Number of days to go back. Default value is 1 day.',
        title='Days Back',
    )
    region: Optional[str] = Field(
        '', 
        description='AWS region. Eg: "us-west-2"', 
        title='Region'
    )


def aws_get_timed_out_lambdas_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_timed_out_lambdas(handle, days_back:int=1, region:str="") -> Tuple:
    """aws_get_timed_out_lambdas finds AWS Lambda functions with high error rate

    :type region: string
    :param region: AWS region. Eg: "us-west-2"

    :type days_back: int
    :param days_back: (in days) Number of days to go back. Default value is 1 day.

    :rtype: Tuple with status result and list of Lambda functions that have timed out

    """
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
            # Iterate through the list of functions and filter out the ones that have timed out
            for function in response['Functions']:
                # Get the configuration for the function
                config_response = lambdaClient.get_function_configuration(FunctionName=function['FunctionName'])
                # Check if the function has a timeout set and if it has timed out
                if 'Timeout' in config_response and config_response['Timeout'] > 0:
                    metrics_response = cloudwatchClient.get_metric_data(
                        MetricDataQueries=[
                            {
                                'Id': 'm1',
                                'MetricStat': {
                                    'Metric': {
                                        'Namespace': 'AWS/Lambda',
                                        'MetricName': 'Duration',
                                        'Dimensions': [
                                            {
                                                'Name': 'FunctionName',
                                                'Value': function['FunctionName']
                                            },
                                        ]
                                    },
                                    'Period': 300,
                                    'Stat': 'p90'
                                },
                                'ReturnData': True
                            },
                        ],
                        StartTime=start_time,
                        EndTime=datetime.datetime.now()
                    )

                    # Check if the function has timed out
                    if len(metrics_response['MetricDataResults'][0]['Values'])!=0:
                        if metrics_response['MetricDataResults'][0]['Values'][0] >= config_response['Timeout'] * 1000:
                            lambda_func = {}
                            lambda_func['function_name'] = function['FunctionName']
                            lambda_func['region'] = reg
                            result.append(lambda_func)
                    else:
                        continue
        except Exception:
            pass
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)