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
        description=('End date till which daily costs are to be fetched. '
                     'Note: It should be given in YYYY-MM-DD format. Eg: 2023-04-11'),
        title='End Date',
    )
    region: str = Field(..., description='AWS region.', title='Region')


def aws_get_cost_for_all_services_printer(output):
    if output is None:
        return
    rows = [x.values() for x in output]
    print(tabulate.tabulate(rows, tablefmt="fancy_grid", headers=['Date','Service','Cost']))

def aws_get_cost_for_all_services(
        handle, region:str,
        number_of_months: int="",
        start_date: str="",
        end_date:str=""
        ) -> List:
    """aws_get_cost_for_all_services returns cost for all services

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :type number_of_months: list
        :param number_of_months: List of instance ids.

        :type start_date: list
        :param start_date: List of instance ids.

        :type end_date: list
        :param end_date: List of instance ids.

        :type region: string
        :param region: Region for instance.

        :rtype: List of dicts of all costs per AWS service in a given time period
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
        TimePeriod = {
            'Start': start,
            'End': end
        },
        Granularity='DAILY',
        Metrics = [
            'UnblendedCost',
                ],
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            },
        ],
        )
    except Exception as e:
        raise e
    for daily_cost in response['ResultsByTime']:
        date = daily_cost['TimePeriod']['Start']
        for group in daily_cost['Groups']:
            cost_est = {}
            cost_est["date"] = date
            service_name = group['Keys'][0]
            service_cost = group['Metrics']['UnblendedCost']['Amount']
            cost_est["service_name"] = service_name
            cost_est["service_cost"] = service_cost
            result.append(cost_est)
    return result
