##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
## Note: For this Action to work, you must do a few things on the Google Side.
## The Google Credential used at unSkript has a service email (probably ending in 'iam.gserviceaccount.com')
##you'll need to add this email account as a user in your Google Analyitics Account.
from pydantic import BaseModel, Field
import pprint
from typing import List,Any, Dict
from googleapiclient.discovery import build
import datetime


from __future__ import annotations

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    days: float = Field(..., description='Number of Days to Pull', title='days')
    view_id: str = Field(..., description='Google Analytics View Id', title='view_id')



def google_analytics_printer(output):

    print(output)


def google_analytics(handle, days:float, view_id:str) -> Dict:
    # Replace with your own Google Analytics view ID



    # Initialize the Google Analytics API service
    analytics = build('analyticsreporting', 'v4', credentials=handle)

    # Calculate the start and end dates for the last 30 days
    end_date = datetime.datetime.now().date()
    start_date = end_date - datetime.timedelta(days=days)

    # Define the query to get daily traffic
    query = {
      'reportRequests': [
        {
          'viewId': view_id,
          'dateRanges': [
            {
              'startDate': start_date.strftime('%Y-%m-%d'),
              'endDate': end_date.strftime('%Y-%m-%d')
            }
          ],
          'metrics': [
            {
              'expression': 'ga:users'
            }
          ],
          'dimensions': [
            {
              'name': 'ga:date'
            }
          ],
          'orderBys': [
            {
              'fieldName': 'ga:date',
              'sortOrder': 'ASCENDING'
            }
          ]
        }
      ]
    }

    # Execute the query and get the response
    response = analytics.reports().batchGet(body=query).execute()

    # Extract the daily traffic data from the response
    daily_traffic = response['reports'][0]['data']['rows']
    #print(daily_traffic)
    # Print the daily traffic data
    results = {}
    for row in daily_traffic:
        date = row['dimensions'][0]
        sessions = int(row['metrics'][0]['values'][0])
       # print(f'{date}: {sessions} sessions')
        results[date] = sessions
    return results


