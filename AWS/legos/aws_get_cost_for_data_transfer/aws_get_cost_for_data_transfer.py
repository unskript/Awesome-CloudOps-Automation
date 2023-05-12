##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import tabulate
from dateutil.relativedelta import relativedelta


class InputSchema(BaseModel):
    number_of_months: Optional[float] = Field(
        '',
        description=('Number of months to fetch the daily costs for. '
                     'Eg: 1 (This will fetch all the costs for the last 30 days)'),
        title='Number of Months',
    )
    start_date: Optional[str] = Field(
        '',
        description=('Start date to get the daily costs from. Note: '
                     'It should be given in YYYY-MM-DD format. Eg: 2023-04-11'),
        title='Start Date',
    )
    end_date: Optional[str] = Field(
        '',
        description=('End date till which daily costs are to be fetched. Note: '
                     'It should be given in YYYY-MM-DD format. Eg: 2023-04-11'),
        title='End Date',
    )
    region: str = Field(..., description='AWS region.', title='region')


def aws_get_cost_for_data_transfer_printer(output):
    if output is None:
        return
    rows = [x.values() for x in output]
    print(tabulate.tabulate(
        rows, tablefmt="fancy_grid",
        headers=['Date','Usage Type','Total Usage Qty','Total Usage Cost']
        ))

def aws_get_cost_for_data_transfer(
        handle,
        region:str,
        number_of_months: int="",
        start_date: str="",
        end_date:str=""
        ) -> List:
    """aws_get_cost_for_data_trasfer returns daily cost spendings on data transfer

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :type number_of_months: int
        :param number_of_months: Optional, Number of months to fetch the daily costs for. 
        Eg: 1 (This will fetch all the costs for the last 30 days)

        :type start_date: string
        :param start_date: Optional, Start date to get the daily costs from. Note: 
        It should be given in YYYY-MM-DD format. Eg: 2023-03-11

        :type end_date: string
        :param end_date: Optional, End date till which daily costs are to be fetched. 
        Note: It should be given in YYYY-MM-DD format. Eg: 2023-04-11

        :type region: string
        :param region: AWS Region.

        :type region: string
        :param region: Region for instance.

        :rtype: List of dicts with data transfer costs
    """
    if number_of_months:
        no_of_months = int(number_of_months)
        end = datetime.date.today().strftime('%Y-%m-%d')
        start = (datetime.date.today() + relativedelta(months=-no_of_months)).strftime('%Y-%m-%d')
    elif not start_date and not end_date and not number_of_months:
        no_of_months = 1
        end = datetime.date.today().strftime('%Y-%m-%d')
        start = (datetime.date.today() + relativedelta(months=-no_of_months)).strftime('%Y-%m-%d')
    else:
        start = start_date
        end = end_date
    result = []
    CEclient = handle.client('ce', region_name=region)
    try:
        response = CEclient.get_cost_and_usage(
        TimePeriod={
            'Start': start,
            'End': end
        },
        Granularity='DAILY',
        Metrics=[
            'UsageQuantity',
            'BlendedCost',
        ],
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'USAGE_TYPE'
            },
        ],
        Filter={
            'Dimensions': {
                'Key': 'USAGE_TYPE',
                'Values': [
                    'DataTransfer-Out-Bytes',
                    'DataTransfer-In-Bytes',
                ],
            },
        },
        )
    except Exception as e:
        raise e
    for daily_cost in response['ResultsByTime']:
        date = daily_cost['TimePeriod']['Start']
        total_cost = 0
        total_usage = 0
        for group in daily_cost['Groups']:
            cost_est = {}
            usage_type = group['Keys'][0]
            usage_quantity = float(group['Metrics']['UsageQuantity']['Amount']) / (1024 ** 4)
            usage_cost = group['Metrics']['BlendedCost']['Amount']
            total_usage += usage_quantity
            total_cost += float(usage_cost)
            cost_est["date"] = date
            cost_est["usage_type"] = usage_type
            cost_est["total_usage"] = round(total_usage,3)
            cost_est["total_cost"] = total_cost
            result.append(cost_est)
    return result
