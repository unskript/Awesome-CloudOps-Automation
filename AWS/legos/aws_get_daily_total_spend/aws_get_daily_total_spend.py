##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict, List
import tabulate
from dateutil.relativedelta import *
import datetime

from typing import Optional

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    number_of_months: Optional[int] = Field(
        '',
        description='Number of months to fetch the daily costs for. Eg: 1 (This will fetch all the costs for the last 30 days)',
        title='Number of months',
    )
    start_date: Optional[str] = Field(
        '',
        description='Start date to get the daily costs from. Note: It should be given in YYYY-MM-DD format. Eg: 2023-03-11',
        title='Start Date',
    )
    end_date: Optional[str] = Field(
        '',
        description='End date till which daily costs are to be fetched. Note: It should be given in YYYY-MM-DD format. Eg: 2023-04-11',
        title='End Date',
    )
    region: str = Field(..., description='AWS region.', title='Region')


def aws_get_daily_total_spend_printer(output):
    if output is None:
        return
    rows = [x.values() for x in output]
    print(tabulate.tabulate(rows, tablefmt="fancy_grid", headers=['Date', 'Cost']))

def aws_get_daily_total_spend(handle, region:str,number_of_months: int="", start_date: str="", end_date:str="") -> List:
    """aws_get_daily_total_spend returns daily cost spendings

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :type number_of_months: int
        :param number_of_months: Optional, Number of months to fetch the daily costs for. Eg: 1 (This will fetch all the costs for the last 30 days)

        :type start_date: string
        :param start_date: Optional, Start date to get the daily costs from. Note: It should be given in YYYY-MM-DD format. Eg: 2023-03-11

        :type end_date: string
        :param end_date: Optional, End date till which daily costs are to be fetched. Note: It should be given in YYYY-MM-DD format. Eg: 2023-04-11

        :type region: string
        :param region: AWS Region.

        :rtype: List of dicts with costs on the respective dates
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
    client = handle.client('ce', region_name=region)
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Granularity='DAILY',
            Metrics=[
                'BlendedCost',
            ]
        )
    except Exception as e:
        raise e
    for daily_cost in response['ResultsByTime']:
        daily_cost_est = {}
        date = daily_cost['TimePeriod']['Start']
        cost = daily_cost['Total']['BlendedCost']['Amount']
        daily_cost_est["date"] = date
        daily_cost_est["cost"] = cost
        result.append(daily_cost_est)
    return result

